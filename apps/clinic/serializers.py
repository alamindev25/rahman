from rest_framework import serializers
from .models import (
    ClinicRegister,
    ClinicProfile,
    ClinicImage,
    ClinicInsurance,
    ClinicTreatment,
    ClinicFacility,
    ClinicAcceptedPatients,
    ClinicPaymentMethod,
    ClinicAvailability,
    ClinicRating,
)
class AcceptedInfectiousField(serializers.Field):
    def to_internal_value(self, data):
        import json
        if data is None:
            return []
        if isinstance(data, str):
            val = data.strip()
            if not val:
                return []
            if (val.startswith('{') and val.endswith('}')) or (val.startswith('[') and val.endswith(']')):
                try:
                    data = json.loads(val)
                except Exception:
                    data = [x.strip() for x in val.split(',') if x.strip()]
            else:
                data = [x.strip() for x in val.split(',') if x.strip()]

        if isinstance(data, list):
            result = []
            for item in data:
                if isinstance(item, dict):
                    name = item.get('patient_name') or item.get('name') or item.get('title') or item.get('label')
                    if name:
                        result.append(str(name))
                    elif item:
                        result.append(item)
                elif isinstance(item, str):
                    s_item = item.strip()
                    if (s_item.startswith('{') and s_item.endswith('}')) or (s_item.startswith('[') and s_item.endswith(']')):
                        try:
                            parsed = json.loads(s_item)
                            if isinstance(parsed, list):
                                result.extend([str(x) for x in parsed])
                            elif isinstance(parsed, dict):
                                name = parsed.get('patient_name') or parsed.get('name')
                                if name:
                                    result.append(str(name))
                        except Exception:
                            if s_item:
                                result.append(s_item)
                    elif s_item:
                        result.append(s_item)
                elif item:
                    result.append(str(item))
            return result

        if isinstance(data, dict):
            return data

        return []

    def to_representation(self, value):
        return value if value is not None else []


class ClinicRegisterSerializer(serializers.ModelSerializer):
    medical_license_document_url = serializers.SerializerMethodField(read_only=True)
    accreditation_authority = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    facility_license_number = serializers.CharField(required=False, allow_blank=True, allow_null=True)
    accepted_infectious = AcceptedInfectiousField(required=False, default=list)

    class Meta:
        model = ClinicRegister
        fields = [
            "id",
            "owner",
            "clinic_name",
            "contact_person",
            "email",
            "phone_number",
            "clinic_group",
            "status",
            "join_network",
            "privacy_and_terms_accepted",
            "facility_license_number",
            "accreditation_authority",
            "medical_license_document",
            "medical_license_document_url",
            "compliance_confirmed",
            "public_activation",
            # "rejection_reason",
            "accepted_infectious",
            "total_beds",
            "created_at",
            "updated_at",
        ]

    def to_internal_value(self, data):
        if hasattr(data, 'getlist'):
            data_dict = {}
            for key in data.keys():
                if key in ['accepted_infectious', 'accepted_patients', 'accepted_patient_categories', 'isolation_units', 'accepted_infectious[]', 'accepted_patients[]']:
                    list_val = data.getlist(key)
                    data_dict[key] = list_val if len(list_val) > 1 else (list_val[0] if list_val else [])
                else:
                    data_dict[key] = data[key]
            data = data_dict
        elif hasattr(data, 'copy'):
            data = data.copy()
        elif hasattr(data, 'dict'):
            data = data.dict()

        if 'accepted_infectious' not in data or not data['accepted_infectious']:
            for key in ['accepted_patients', 'accepted_patient_categories', 'isolation_units', 'accepted_infectious[]', 'accepted_patients[]']:
                if key in data and data[key]:
                    data['accepted_infectious'] = data[key]
                    break

        categories = []
        if data.get('hiv_positive') in [True, 'true', 'True', 1, '1'] or data.get('hiv') in [True, 'true', 'True', 1, '1']:
            categories.append('HIV Positive Patients')
        if data.get('hbv_positive') in [True, 'true', 'True', 1, '1'] or data.get('hbv') in [True, 'true', 'True', 1, '1'] or data.get('hepatitis_b') in [True, 'true', 'True', 1, '1']:
            categories.append('Hepatitis B (HBV+)')
        if data.get('hcv_positive') in [True, 'true', 'True', 1, '1'] or data.get('hcv') in [True, 'true', 'True', 1, '1'] or data.get('hepatitis_c') in [True, 'true', 'True', 1, '1']:
            categories.append('Hepatitis C (HCV+)')

        if categories and ('accepted_infectious' not in data or not data['accepted_infectious']):
            data['accepted_infectious'] = categories

        if 'accreditation_authority' in data:
            val = data['accreditation_authority']
            if hasattr(val, 'read') or hasattr(val, 'chunks'):
                if 'medical_license_document' not in data or not data['medical_license_document']:
                    data['medical_license_document'] = val
                data['accreditation_authority'] = str(getattr(val, 'name', ''))

        return super().to_internal_value(data)

    def get_medical_license_document_url(self, obj):
        request = self.context.get('request')
        if obj.medical_license_document:
            if request:
                return request.build_absolute_uri(obj.medical_license_document.url)
            return obj.medical_license_document.url
        return None

    def _sync_accepted_patients(self, clinic):
        if hasattr(clinic, 'profile') and clinic.profile:
            profile = clinic.profile
            accepted_infectious = clinic.accepted_infectious
            if isinstance(accepted_infectious, list):
                profile.accepted_patients.all().delete()
                for item in accepted_infectious:
                    name = item.get('patient_name') if isinstance(item, dict) else str(item)
                    if name:
                        ClinicAcceptedPatients.objects.create(clinic=profile, patient_name=name)
            elif isinstance(accepted_infectious, dict):
                profile.accepted_patients.all().delete()
                for key, val in accepted_infectious.items():
                    if val:
                        ClinicAcceptedPatients.objects.create(clinic=profile, patient_name=str(key))

    def create(self, validated_data):
        user = self.context["request"].user
        clinic = ClinicRegister.objects.create(
            owner=user,
            status=ClinicRegister.Status.PENDING,
            **validated_data
        )
        if user.role != "CLINIC_OWNER":
            user.role = "CLINIC_OWNER"
            user.save()
        self._sync_accepted_patients(clinic)
        return clinic

    def update(self, instance, validated_data):
        clinic = super().update(instance, validated_data)
        self._sync_accepted_patients(clinic)
        return clinic
class ClinicImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    class Meta:
        model = ClinicImage
        fields = [
            'id',
            'image',
            'image_url',
        ]
        read_only_fields = ['clinic']
    def get_image_url(self, obj):
        request = self.context.get('request')
        print("REQUEST =", request)
        if obj.image:
            if request:
                return request.build_absolute_uri(obj.image.url)
            return obj.image.url
        return None

# ClinicInsurance Serializer
class ClinicInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicInsurance
        fields = "__all__"
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'insurance_name': data}
        return super().to_internal_value(data)

# ClinicTreatment Serializer
class ClinicTreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicTreatment
        fields = "__all__"
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'treatment_name': data}
        return super().to_internal_value(data)

# ClinicFacility Serializer
class ClinicFacilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicFacility
        fields = "__all__"
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'facility_name': data}
        return super().to_internal_value(data)

# ClinicAcceptedPatients Serializer
class ClinicAcceptedPatientsSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAcceptedPatients
        fields = "__all__"
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'patient_name': data}
        return super().to_internal_value(data)

# ClinicPaymentMethod Serializer
class ClinicPaymentMethodSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicPaymentMethod
        fields = "__all__"
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if isinstance(data, str):
            data = {'payment_method_name': data}
        return super().to_internal_value(data)

# ClinicAvailability Serializer
class ClinicAvailabilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAvailability
        fields = "__all__"
        read_only_fields = ['clinic']

# ClinicRating Serializer
class ClinicRatingSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicRating
        fields = ['clinic', 'rating']

    def validate(self, data):
        user = self.context['request'].user
        clinic = data['clinic']
        if user and user.is_authenticated:
            if ClinicRating.objects.filter(clinic=clinic, user=user).exists():
                raise serializers.ValidationError("You have already rated this clinic.")
        return data

# ClinicGetProfile Serializer
class ClinicGetProfileSerializer(serializers.ModelSerializer):
    images = ClinicImageSerializer(many=True, read_only=True)
    treatments = ClinicTreatmentSerializer(many=True, read_only=True)
    facilities = ClinicFacilitySerializer(many=True, read_only=True)
    insurances = ClinicInsuranceSerializer(many=True, read_only=True)
    ratings = ClinicRatingSerializer(many=True, read_only=True)
    accepted_patients = ClinicAcceptedPatientsSerializer(many=True, read_only=True)
    accepted_infectious = serializers.SerializerMethodField()
    average_rating = serializers.SerializerMethodField()

    class Meta:
        model = ClinicProfile
        fields = [
            'id',
            'clinic',
            'name',
            'title',
            'country',
            'city',
            'address',
            'distance_from_city_center',
            'per_treatment_price',
            'images',
            'treatments',
            'ratings',
            'facilities',
            'insurances',
            'accepted_patients',
            'accepted_infectious',
            'average_rating',
        ]

    def get_average_rating(self, obj):
        return obj.get_average_rating()

    def get_accepted_infectious(self, obj):
        if obj.clinic and obj.clinic.accepted_infectious:
            return obj.clinic.accepted_infectious
        return [p.patient_name for p in obj.accepted_patients.all()]


# ClinicProfile Serializer (Nested Serializer for Read, Create & Update)
class ClinicProfileSerializer(serializers.ModelSerializer):
    # clinic_details = ClinicRegisterSerializer(source='clinic', read_only=True)
    images = ClinicImageSerializer(many=True, read_only=True)
    treatments = ClinicTreatmentSerializer(many=True, required=False)
    facilities = ClinicFacilitySerializer(many=True, required=False)
    insurances = ClinicInsuranceSerializer(many=True, required=False)
    accepted_patients = ClinicAcceptedPatientsSerializer(many=True, required=False)
    accepted_infectious = serializers.SerializerMethodField()
    payment_methods = ClinicPaymentMethodSerializer(many=True, required=False)
    availabilities = ClinicAvailabilitySerializer(many=True, required=False)

    class Meta:
        model = ClinicProfile
        fields = [
            'id',
            'clinic',
            'name',
            'title',
            'description',
            'country',
            'city',
            'address',
            'distance_from_city_center',
            'latitude',
            'longitude',
            'per_treatment_price',
            'images',
            'treatments',
            'facilities',
            'insurances',
            'accepted_patients',
            'accepted_infectious',
            'payment_methods',
            'availabilities'
        ]
        read_only_fields = ['clinic']

    def to_internal_value(self, data):
        if hasattr(data, 'copy'):
            data = data.copy()
        elif hasattr(data, 'dict'):
            data = data.dict()

        if 'accepted_patients' not in data or not data['accepted_patients']:
            if 'accepted_infectious' in data and data['accepted_infectious']:
                data['accepted_patients'] = data['accepted_infectious']

        return super().to_internal_value(data)

    def get_accepted_infectious(self, obj):
        if obj.clinic and obj.clinic.accepted_infectious:
            return obj.clinic.accepted_infectious
        return [p.patient_name for p in obj.accepted_patients.all()]

    def _sync_accepted_patients_data(self, profile, accepted_patients_data):
        if accepted_patients_data is not None:
            profile.accepted_patients.all().delete()
            patient_names = []
            for patient in accepted_patients_data:
                if isinstance(patient, str):
                    ClinicAcceptedPatients.objects.create(clinic=profile, patient_name=patient)
                    patient_names.append(patient)
                elif isinstance(patient, dict):
                    name = patient.get('patient_name') or patient.get('name') or patient.get('title')
                    if name:
                        ClinicAcceptedPatients.objects.create(clinic=profile, patient_name=name)
                        patient_names.append(name)

            if profile.clinic:
                profile.clinic.accepted_infectious = patient_names
                profile.clinic.save(update_fields=['accepted_infectious'])

    def create(self, validated_data):
        treatments_data = validated_data.pop('treatments', [])
        facilities_data = validated_data.pop('facilities', [])
        insurances_data = validated_data.pop('insurances', [])
        accepted_patients_data = validated_data.pop('accepted_patients', [])
        payment_methods_data = validated_data.pop('payment_methods', [])
        availabilities_data = validated_data.pop('availabilities', [])
        profile = ClinicProfile.objects.create(**validated_data)
        for treatment in treatments_data:
            ClinicTreatment.objects.create(clinic=profile, **treatment)
        for facility in facilities_data:
            ClinicFacility.objects.create(clinic=profile, **facility)
        for insurance in insurances_data:
            ClinicInsurance.objects.create(clinic=profile, **insurance)
        for payment in payment_methods_data:
            ClinicPaymentMethod.objects.create(clinic=profile, **payment)
        for availability in availabilities_data:
            ClinicAvailability.objects.create(clinic=profile, **availability)

        self._sync_accepted_patients_data(profile, accepted_patients_data)

        return profile

    def update(self, instance, validated_data):
        treatments_data = validated_data.pop('treatments', None)
        facilities_data = validated_data.pop('facilities', None)
        insurances_data = validated_data.pop('insurances', None)
        accepted_patients_data = validated_data.pop('accepted_patients', None)
        payment_methods_data = validated_data.pop('payment_methods', None)
        availabilities_data = validated_data.pop('availabilities', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if treatments_data is not None:
            instance.treatments.all().delete()
            for treatment in treatments_data:
                ClinicTreatment.objects.create(clinic=instance, **treatment)

        if facilities_data is not None:
            instance.facilities.all().delete()
            for facility in facilities_data:
                ClinicFacility.objects.create(clinic=instance, **facility)
        if insurances_data is not None:
            instance.insurances.all().delete()
            for insurance in insurances_data:
                ClinicInsurance.objects.create(clinic=instance, **insurance)

        self._sync_accepted_patients_data(instance, accepted_patients_data)

        if payment_methods_data is not None:
            instance.payment_methods.all().delete()
            for payment in payment_methods_data:
                ClinicPaymentMethod.objects.create(clinic=instance, **payment)

        if availabilities_data is not None:
            instance.availabilities.all().delete()
            for availability in availabilities_data:
                ClinicAvailability.objects.create(clinic=instance, **availability)
        request = self.context.get('request')
        
        if request:
            images = request.FILES.getlist('images')

            for image in images:
                ClinicImage.objects.create(
                    clinic=instance,
                    image=image
                )
        return instance


class ClinicSubmissionStatusSerializer(serializers.ModelSerializer):
    submitted_clinic = serializers.CharField(source='clinic_name', read_only=True)
    contact_email = serializers.SerializerMethodField(read_only=True)
    facility_license_number = serializers.CharField(read_only=True)
    status_badge = serializers.SerializerMethodField(read_only=True)
    title = serializers.SerializerMethodField(read_only=True)
    description = serializers.SerializerMethodField(read_only=True)
    notice = serializers.SerializerMethodField(read_only=True)
    estimated_assessment_time = serializers.SerializerMethodField(read_only=True)
    is_email_verified = serializers.SerializerMethodField(read_only=True)
    # what_happens_next = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = ClinicRegister
        fields = [
            "id",
            "status",
            "status_badge",
            "title",
            "description",
            "notice",
            "submitted_clinic",
            "contact_email",
            "facility_license_number",
            "estimated_assessment_time",
            "is_email_verified",
            "rejection_reason",
            # "what_happens_next",
            "created_at",
            "updated_at",
        ]

    def get_contact_email(self, obj):
        if obj.email:
            return obj.email
        if obj.owner and obj.owner.email:
            return obj.owner.email
        return ""

    def get_status_badge(self, obj):
        if obj.status == ClinicRegister.Status.APPROVED:
            return "APPLICATION APPROVED"
        elif obj.status == ClinicRegister.Status.REJECTED:
            return "APPLICATION REJECTED"
        return "APPLICATION RECEIVED • UNDER REVIEW"

    def get_title(self, obj):
        if obj.status == ClinicRegister.Status.APPROVED:
            return "Your Request Has Been Approved!"
        elif obj.status == ClinicRegister.Status.REJECTED:
            return "Your Application Needs Attention"
        return "Your Request Has Been Submitted!"

    def get_description(self, obj):
        if obj.status == ClinicRegister.Status.APPROVED:
            return "Your clinic registration and medical documents have been approved by our Medical Compliance Team."
        elif obj.status == ClinicRegister.Status.REJECTED:
            return "Your clinic registration was not approved. Please check the rejection reason below."
        return "Your clinic registration and medical documents are currently under review by our Medical Compliance Team."

    def get_notice(self, obj):
        return "For further assessment, review updates, and email verification, please check your mail."

    def get_estimated_assessment_time(self, obj):
        return "24 – 48 Hours"

    def get_is_email_verified(self, obj):
        if obj.owner:
            return getattr(obj.owner, 'is_verified', False)
        return False

    # def get_what_happens_next(self, obj):
    #     return [
    #         "Open your inbox and verify your email address using the confirmation code.",
    #         "Our medical administration team audits your facility license and serology safety protocols.",
    #         "Once approved by Super Admin, your clinic will go live on the MedBook search marketplace!"
    #     ]






    