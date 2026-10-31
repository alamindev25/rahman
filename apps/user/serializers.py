
from google_crc32c import value

from google_crc32c import value

from apps.system_setting.models import AboutSystem, SystemColor
from .models import  User, UserProfile, OTP
from rest_framework import  serializers
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.hashers import make_password
from django.utils.timezone import timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings
from .utils import generate_otp
from django.utils import timezone
from apps.utils.helpers import success, error
from apps.utils.tasks import send_email_task
from django.template.loader import render_to_string
from .utils import get_user_agent_hash, get_cloudinary_url
from rest_framework import serializers
# from .models import ClinicRating

def _build_email_template_context(extra_context=None):
    system_info = AboutSystem.objects.first()
    system_color = (
        SystemColor.objects.filter(is_active=True)
        .values_list('code', flat=True)
        .first()
        or '#204452'
    )
    context = {
        'system_info': system_info,
        'system_color': system_color,
    }

    if extra_context:
        context.update(extra_context)

    return context

class CustomRefreshToken(RefreshToken):
    @classmethod
    def for_user(cls, user, remember_me=False, user_agent_hash=None):
        token = super().for_user(user)

        token["user_id"] = user.id
        token["role"] = user.role
        token["uah"] = user_agent_hash

        if remember_me:
            token.set_exp(lifetime=settings.SIMPLE_JWT["REMEMBER_ME_REFRESH_LIFETIME"])
        else:
            token.set_exp(lifetime=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"])

        return token

# Signup
class SignUpSerializer(serializers.ModelSerializer):
    # user
    full_name = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    privacy_and_terms_accepted = serializers.BooleanField(required=False)
    accepted_terms = serializers.BooleanField(write_only=True, required=False)
    privacy_policy_accepted = serializers.BooleanField(write_only=True, required=False)
    terms_accepted = serializers.BooleanField(write_only=True, required=False)
  
    # user profile
    phone = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    avatar = serializers.ImageField(write_only=True, required=False)
    gender = serializers.CharField(write_only=True, required=False, allow_blank=True, allow_null=True)
    dob = serializers.DateField(write_only=True, required=False, allow_null=True)
    purpose = serializers.CharField(write_only=True)
    account_type = serializers.ChoiceField(choices=[("PATIENT", "Patient"), ("CLINIC_OWNER", "Clinic Owner")], write_only=True, required=True)
    role = serializers.CharField(read_only=True)


    class Meta:
        model = User
        fields = [
            'full_name',
            'email',
            'password',
            'confirm_password',
            'privacy_and_terms_accepted',
            'accepted_terms',
            'privacy_policy_accepted',
            'terms_accepted',
            'account_type',

            'purpose',
            'role',
            'phone',
            'avatar',
            'gender',
            'dob',
        ]

    def validate(self, attrs):
        full_name = (attrs.get('full_name') or '').strip()
        email = attrs.get('email')
        password = attrs.get('password')
        confirm_password = attrs.get('confirm_password')
        account_type = attrs.get('account_type')
        privacy_and_terms_accepted = (
            attrs.get('privacy_and_terms_accepted')
            or attrs.get('accepted_terms')
            or attrs.get('privacy_policy_accepted')
            or attrs.get('terms_accepted')
        )
        purpose = (attrs.get('purpose') or '').strip()

        # full_name required

        if not full_name:
            raise serializers.ValidationError({'full_name': 'Full name is required.'})
        
        # Check email already exists
        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError({'email': 'User with this email already exists.'})
        
        # Validate password
        if not password:
            raise serializers.ValidationError({'password': 'Password is required.'})

        # Check if passwords match
        if password != confirm_password:
            raise serializers.ValidationError({'confirm_password': 'Passwords do not match.'})

        # Check privacy and terms accepted
        if privacy_and_terms_accepted is not True:
            raise serializers.ValidationError({
                'privacy_and_terms_accepted': 'You must accept the privacy and terms to proceed.'
            })
        if account_type not in [User.Roles.PATIENT, User.Roles.USER, User.Roles.CLINIC_OWNER]:
            raise serializers.ValidationError({
                "account_type": "Invalid account type."
            })


        attrs['privacy_and_terms_accepted'] = True
        
        allowed_purposes = {'signup'}
        if purpose and purpose not in allowed_purposes:
            raise serializers.ValidationError({'purpose': 'Invalid purpose.'})

        return attrs

    def create(self, validated_data):
        full_name = (validated_data.pop('full_name', '') or '').strip()
        email = validated_data.pop('email')
        password = validated_data.pop('password')
        account_type = validated_data.pop(
            'account_type'
        )
        avatar = validated_data.pop('avatar', None)
        gender = validated_data.pop('gender', None)
        dob = validated_data.pop('dob', None)
        phone = validated_data.pop('phone', None)
        purpose = validated_data.pop('purpose', None)
        validated_data.pop('accepted_terms', None)
        validated_data.pop('privacy_policy_accepted', None)
        validated_data.pop('terms_accepted', None)

        # Split full_name -> first_name, last_name
        parts = full_name.split()
        first_name = " ".join(parts[:-1]) if len(parts) > 1 else (parts[0] if parts else "")
        last_name = parts[-1] if len(parts) > 1 else ""
        
        # Create user
        user = User.objects.create_user(
            email=email,
            password=password,
            role=account_type,
            privacy_and_terms_accepted=validated_data.get('privacy_and_terms_accepted', False)
        )
        if avatar:
            user.avatar = avatar
            user.save(update_fields=['avatar'])

        # Create profile
        UserProfile.objects.create(
            user=user,
            first_name=first_name,
            last_name=last_name,
            gender=gender,
            dob=dob,
            phone=phone,
            accepted_terms=validated_data.get('privacy_and_terms_accepted', False)  # optional sync
        )

        # OTP create
        otp_code = generate_otp()
        otp_hashed = make_password(otp_code)
        expires_at = timezone.now() + timedelta(minutes=3)

        OTP.objects.update_or_create(
            user=user,
            defaults={
                'otp': otp_hashed,
                'is_verify': False,
                'purpose': purpose or 'signup',
                'created_at': timezone.now(),
                'expires_at': expires_at
            }
        )

        html_content = render_to_string(
            'email/signup_otp_verification_template.html',
            _build_email_template_context({'otp_code': otp_code})
        )

        send_email_task.delay(
            subject='Verification OTP',
            body=f'Your OTP is {otp_code}. Expire in 3 minutes.',
            to_emails=[user.email],
            from_email=settings.EMAIL_HOST_USER,
            html_body=html_content
        )

        return user

    def to_representation(self, instance):
        request = self.context.get('request')
        user_agent_hash = get_user_agent_hash(request) if request else None

        refresh = CustomRefreshToken.for_user(instance, user_agent_hash=user_agent_hash)

        return {
            'user': {
                'id': instance.id,
                'email': instance.email,
                'message': 'User created successfully. Please verify OTP sent to your email to activate your account.',
                'role': instance.role,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }

# Signin
class SignInSerializer(serializers.Serializer):

    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    refresh_token = serializers.CharField(read_only=True)
    access_token = serializers.CharField(read_only=True)
    remember_me = serializers.BooleanField(required=False, default=False)

    def validate(self, attrs):
        password = attrs.get('password')
        user = User.objects.filter(email=attrs['email']).first()
        if not user:
           raise serializers.ValidationError({'email': 'User with this email does not exist.'})
        if not user.check_password(password):
            raise serializers.ValidationError({'password': 'Invalid password.'})
        
        #OTP verification check
        if not user.is_verified: 
            raise serializers.ValidationError({
            'otp': 'Your account is not verified. Please verify OTP first.'
        })

        # Clinic Owner Approval Check
        if user.role == User.Roles.CLINIC_OWNER or user.role in ["CLINIC_ADMIN", "clinic_admin"]:
            from apps.clinic.models import ClinicRegister
            from django.db.models import Q
            clinic = ClinicRegister.objects.filter(
                Q(owner=user) | Q(clinic_admin=user) | Q(email__iexact=user.email)
            ).first()

            if clinic and clinic.status != ClinicRegister.Status.APPROVED:
                if clinic.status == ClinicRegister.Status.REJECTED:
                    reason = getattr(clinic, 'rejection_reason', None) or 'N/A'
                    raise serializers.ValidationError({
                        'clinic': f'Your clinic registration has been rejected. Reason: {reason}'
                    })
                raise serializers.ValidationError({
                    'clinic': 'Your clinic registration is pending approval. You cannot sign in until approved by Admin.'
                })

        self.user = user
        return attrs

    
    def to_representation(self, instance):
        user = self.user
        request = self.context.get('request')

        user_agent_hash = get_user_agent_hash(request) if request else None

        refresh = CustomRefreshToken.for_user(
            user,
            user_agent_hash=user_agent_hash
        )
        return {
            'user': {
                'id': user.id,
                'email': user.email,
                'avatar': get_cloudinary_url(user.avatar) if user.avatar else None,
                'role': user.role,
            },
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

# SignOut
class SignOutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(write_only=True)

    def validate(self, attrs):
        self.refresh_token = attrs.get('refresh_token')
        return attrs
    
    def save(self, **kwargs):
        try:
            token = RefreshToken(self.refresh_token)
            token.blacklist()
        except Exception as e:
            return ValidationError({'error': str(e)})

# Change Password
class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 'confirm_password']

    def validate(self, attrs):
        
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')

        user = self.context['request'].user
        if not user:
            raise ValidationError({'error': 'User not found.'})
        
        if not user.check_password(old_password):
            raise ValidationError({'error': 'Old password is incorrect.'})
        
        if new_password != confirm_password:
            raise ValidationError({'error': 'New password and confirm password is not match.'})
        
        if old_password == new_password:
            raise ValidationError({'error': 'The new password is not the same as the old password.'})
        
        try:
            validate_password(new_password)
        except Exception as e:
            raise ValidationError({'error': str(e.messages)})
        
        self.user = user
        return attrs
    
    def save(self):
        new_password = self.validated_data['new_password']
        user = self.user
        user.set_password(new_password)
        user.save()
        return user

# Forgot Password (OTP Send)
class SendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.CharField()

    def validate(self, attrs):
        try:
            user = User.objects.get(email=attrs['email'])
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': 'User not found.'})
        
        otp_code = generate_otp()
        otp_hashed = make_password(otp_code)
        purpose = attrs['purpose']

        expires_at = timezone.now() + timedelta(minutes=3)

        OTP.objects.update_or_create(user=user, defaults={'otp': otp_hashed, 'is_verify': False, 'purpose': purpose, 'created_at': timezone.now(), 'expires_at': expires_at})
        
        html_content = render_to_string(
            'email/forgetpass_otp_verification_template.html',
            _build_email_template_context({'otp_code': otp_code})
        )

        try:
          send_email_task.delay(
                subject='Verification OTP',
                body=f'Your OTP is {otp_code}. Expire in 3 minutes.',
                to_emails=[user.email,],
                from_email=settings.EMAIL_HOST_USER,
                html_body=html_content
                )
        except:
            raise serializers.ValidationError("SMTP NOT VALID!")
        return attrs

# Reset Password (OTP Verify and Reset)
class ResetPasswordSerializer(serializers.Serializer):

    email = serializers.EmailField()
    purpose = serializers.CharField()
    new_password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data['email']
        purpose = data['purpose']
        new_password = data['new_password']
        confirm_password = data['confirm_password']

        try:
            user = User.objects.get(email=email)
            otp_obj = OTP.objects.get(user=user, purpose=purpose)
        except (User.DoesNotExist, OTP.DoesNotExist):
            raise serializers.ValidationError({'error': "Invalid credentials or OTP."})

        if otp_obj.is_expired():
            otp_obj.delete()
            raise serializers.ValidationError({'error': "OTP has expired."})
        
        if not otp_obj.is_verify:
            raise serializers.ValidationError({'error': 'OTP not verified yet. Please verify OTP first.'})
        if new_password != confirm_password:
            raise serializers.ValidationError({'error': "Passwords do not match."})
        try:
            validate_password(new_password, user)
        except serializers.ValidationError as e:
            raise serializers.ValidationError({'error': str(e.messages)})

        data['user'] = user
        return data

    def save(self):
        user = self.validated_data['user']
        new_password = self.validated_data['new_password']
        user.set_password(new_password)
        user.save()
        OTP.objects.filter(user=user, purpose=self.validated_data['purpose']).delete()

# Resend OTP
class ResendOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    purpose = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        purpose = (attrs.get('purpose') or '').strip()

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist as e:
            raise serializers.ValidationError({'error': 'User not found.'})

        if not purpose:
            raise serializers.ValidationError({'purpose': 'Purpose is required.'})

        if purpose == 'signup' and user.is_verified:
            raise serializers.ValidationError({'error': 'Account is already verified.'})
        
        otp_code = generate_otp()
        otp_hashed = make_password(otp_code)
        expires_at = timezone.now() + timedelta(minutes=3)

        OTP.objects.update_or_create(
            user=user,
            purpose=purpose,
            defaults={
                'otp': otp_hashed,
                'is_verify': False,
                'attempts': 0,
                'created_at': timezone.now(),
                'expires_at': expires_at,
            }
        )

        template_name = (
            'email/signup_otp_verification_template.html'
            if purpose == 'signup'
            else 'email/forgetpass_otp_verification_template.html'
        )

        html_content = render_to_string(
            template_name,
            _build_email_template_context({'otp_code': otp_code})
        )

        email_payload = {
            'subject': 'Verification OTP',
            'body': f'Your OTP is {otp_code}. Expire in 3 minutes.',
            'to_emails': [user.email],
            'from_email': settings.EMAIL_HOST_USER,
            'html_body': html_content,
        }

        try:
            send_email_task(**email_payload)
        except Exception:
            raise serializers.ValidationError({'error': 'SMTP NOT VALID!'})
        return attrs



class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    purpose = serializers.CharField()

    def validate(self, data):
        email = data.get("email")
        otp_input = data.get("otp")
        purpose = data.get("purpose")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise serializers.ValidationError({'error': "Invalid email."})

        try:
            otp_obj = OTP.objects.get(user=user, purpose=purpose)
        except OTP.DoesNotExist:
            raise serializers.ValidationError({'error': "OTP not found. Please request a new one."})

        if otp_obj.is_verify:
            raise serializers.ValidationError({'error': "OTP already vrified."})

        if otp_obj.is_expired():
            otp_obj.delete()
            raise serializers.ValidationError({'error': "OTP expired. Please request a new one."})

        if not otp_obj.check_otp(otp_input):
            otp_obj.attempts += 1
            if otp_obj.attempts >= 3:
                otp_obj.delete()
                raise serializers.ValidationError({'error': "Too many incorrect attempts. Please request a new one."})
            otp_obj.save()
            raise serializers.ValidationError({'error': f"Incorrect OTP. Attempt {otp_obj.attempts}/3."})

        self.user = user
        self.otp_obj = otp_obj
        return data

    def save(self):
        # OTP verified
        self.otp_obj.is_verify = True
        self.otp_obj.attempts = 0
        self.otp_obj.save()

        # Handle different purposes
        if self.otp_obj.purpose == 'signup':
            self.user.is_verified = True
            self.user.save()
            
        elif self.otp_obj.purpose == 'password_reset':
            return {
                'id': self.user.id,
                'email': self.user.email,
                'message': 'OTP verified successfully.',
                'verified': True
            }

        # Generate tokens for signup and other purposes
        request = self.context.get('request')
        user_agent_hash = get_user_agent_hash(request) if request else None
        refresh = CustomRefreshToken.for_user(
            self.user,
            remember_me=False,
            user_agent_hash=user_agent_hash
        )
        
        return {
            'user': {
            'id': self.user.id,
            'email': self.user.email,
            'avatar': get_cloudinary_url(self.user.avatar) if self.user.avatar else None,
            'is_verified': self.user.is_verified,
        },
        'access_token': str(refresh.access_token),
        'refresh_token': str(refresh)
    }

# Profile Update Avatar
class UpdateProfileAvatarSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField(required=False, allow_null=True)
    class Meta:
        model = User
        fields = ['avatar']

    def update(self, instance, validated_data):
        avatar = validated_data.get('avatar', None)
        if avatar is not None:
            instance.avatar = avatar
            instance.save(update_fields=['avatar'])
        return instance

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        ret['avatar'] = get_cloudinary_url(instance.avatar) if instance.avatar else None
        return ret

#user

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = [
            "id",
            "email",
            "is_staff",
            "is_active",
            "date_joined",
            "profile",
        ]

# UserProfile
class UserProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "full_name",
            "email",
            "phone",
            "country",
            "gender",
            "dob",
            "nationality",
            "address",
            # "linkedin",
            # "github",
            # "twitter",
        ]

    def to_representation(self, instance):
        # Compute full name and preserve the order specified in Meta.fields
        computed_full_name = f"{instance.first_name} {instance.last_name}".strip()
        ret = super().to_representation(instance)

        ordered = {}
        for field in self.Meta.fields:
            if field == 'full_name':
                ordered['full_name'] = computed_full_name
            elif field == 'email':
                ordered['email'] = instance.user.email if hasattr(instance, 'user') and instance.user else None
            else:
                ordered[field] = ret.get(field)
        return ordered
        
    def _split_full_name(self, full_name):
        parts = (full_name or '').strip().split()
        first_name = " ".join(parts[:-1]) if len(parts) > 1 else (parts[0] if parts else "")
        last_name = parts[-1] if len(parts) > 1 else ""
        return first_name, last_name

    def create(self, validated_data):
        full_name = validated_data.pop('full_name', None)
        if full_name is not None:
            first_name, last_name = self._split_full_name(full_name)
            validated_data['first_name'] = first_name
            validated_data['last_name'] = last_name
        return super().create(validated_data)

    def update(self, instance, validated_data):
        # Update first/last name when full_name is supplied, then update other fields
        full_name = validated_data.pop('full_name', None)
        if full_name is not None:
            first_name, last_name = self._split_full_name(full_name)
            instance.first_name = first_name
            instance.last_name = last_name
        return super().update(instance, validated_data)

# Get UserProfile
class UserProfileGetSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(source='user.avatar')
    email = serializers.EmailField(source='user.email', read_only=True)
    name = serializers.SerializerMethodField()
    joining_date = serializers.SerializerMethodField()

    class Meta:
        model = UserProfile
        fields = [
            "id",
            "avatar",
            "name",
            "email",
            "nationality",
            "phone",
            "country",
            "gender",
            "dob",
            "address",
            "joining_date",
            # "linkedin",
            # "github",
            # "twitter",
        ]

    def get_avatar(self, obj):
        if obj.user.avatar:
            return get_cloudinary_url(obj.user.avatar)
        return None

    def get_name(self, obj):
        return f"{obj.first_name} {obj.last_name}".strip()
    
    def get_joining_date(self, obj):
        if obj.user.created_at:
            return obj.user.created_at.strftime("%d %B %Y")
        return None
    


    
# class ClinicRatingSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = ClinicRating
#         fields = ['clinic', 'rating']

#     def validate(self, data):
        
#         user = self.context['request'].user
#         clinic = data['clinic']

#         if ClinicRating.objects.filter(clinic=clinic, user=user).exists():
#             raise serializers.ValidationError("You have already rated this clinic.")
        
#         return data


# class ClinicListingUpdataSerializer(serializers.ModelSerializer):
#     average_rating = serializers.SerializerMethodField()

#     class Meta:
#         model = Clinic
#         fields = [
#             'id', 'clinic_name', 'image', 'location', 'distance', 
#             'has_ehic', 'has_ghic', 'has_refreshments', 
#             'has_free_transfer', 'has_free_parking', 
#             'price_hd', 'price_hdf', 'average_rating'
#         ]
#     def get_average_rating(self, obj):
#         return obj.get_average_rating()

 


# class ClinicListingSerializer(serializers.ModelSerializer):

    
#     class Meta:
#         model = Clinic
#         fields = [
#             'id', 'clinic_name', 'contact_person', 'email', 
#             'phone_number', 'clinic_group', 'status',
#             'join_network', 'privacy_and_terms_accepted' # Fields added
#         ]
#         read_only_fields = ['status']


#     # Form level dynamic privacy check constraint rule structure logic mapping validation handler
    
#     def validate_privacy_and_terms_accepted(self, value):
#         if value is not True:
#             raise serializers.ValidationError(
#                 "You must accept the terms, privacy policy, and data processing rules to list your clinic."
#             )
#         return value
    


# 2. Clinic Admin Appointment Dynamic Overview Tracker
# class ClinicAppointmentSerializer(serializers.ModelSerializer):
#     patient = PatientProfileSerializer(read_only=True)

#     class Meta:
#         model = Appointment
#         fields = ['id', 'patient', 'appointment_date', 'symptoms', 'created_at']
