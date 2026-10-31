from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from datetime import timedelta
from .managers import UserManager
from django.contrib.auth.hashers import check_password
from cloudinary.models import CloudinaryField

class User(AbstractBaseUser, PermissionsMixin):
    class Roles(models.TextChoices):
        PATIENT = "PATIENT", "Patient"
        CLINIC_OWNER = "CLINIC_OWNER", "Clinic Owner"
        ADMIN = "ADMIN", "Admin"

    Roles.USER = Roles.PATIENT
    email = models.EmailField(_("email address"), unique=True)
    avatar = CloudinaryField('avatar', blank=True, null=True)
    role = models.CharField(max_length=20, choices=Roles.choices, default=Roles.PATIENT)
    is_verified = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    privacy_and_terms_accepted = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["privacy_and_terms_accepted"]
    objects = UserManager()

    def __str__(self):
        return self.email

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    country=models.CharField(max_length=100, blank=True, null=True) 
    gender = models.CharField(max_length=10, blank=True, null=True)
    accepted_terms = models.BooleanField(default=False)
    dob = models.DateField(blank=True, null=True)
    nationality = models.CharField(max_length=100, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    github = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}" if self.first_name or self.last_name else self.user.email

PURPOSE = (
    ('password_reset', 'Password Reset'),
    ('login', 'Login'),
    ('delete_account', 'Delete Account'),
    ('account_create', 'Account Create')
)

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='otps')
    otp = models.CharField(max_length=255)
    is_verify = models.BooleanField(default=False)
    attempts = models.IntegerField(default=0)
    purpose = models.CharField(max_length=50, blank=True, null=True, choices=PURPOSE) # login, password reset, 2fa etc
    created_at = models.DateTimeField(auto_now_add=True)
    expires_at = models.DateTimeField()

    def save(self, *args, **kwargs):
        if not self.expires_at:
            self.expires_at = timezone.now() + timedelta(minutes=3)
        super().save(*args, **kwargs)

    def is_expired(self):
        return timezone.now() > self.expires_at

    def check_otp(self, raw_otp):
        return check_password(raw_otp, self.otp)
    

# class Clinic(models.Model):
#     class Status(models.TextChoices):
#         PENDING = 'pending', _('Pending Approval')
#         APPROVED = 'approved', _('Approved')


#     from apps.clinic.models import Clinic, ClinicRating  # re-export for backward compatibility
# class Clinic(models.Model):

#     class Status(models.TextChoices):

#         PENDING = 'pending', _('Pending Approval')

#         APPROVED = 'approved', _('Approved')

#         REJECTED = 'rejected', _('Rejected')
