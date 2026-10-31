from django.conf import settings
from django.db import models
from django.db.models import Avg
from django.utils.translation import gettext_lazy as _
from apps.user.models import User

# Clinic Registration
class ClinicRegister(models.Model):
    class Status(models.TextChoices):
        PENDING = 'pending', _('Pending Approval')
        APPROVED = 'approved', _('Approved')
        REJECTED = 'rejected', _('Rejected')
    owner= models.ForeignKey(User, on_delete=models.CASCADE, related_name='clinic', null=True, blank=True)
    clinic_name = models.CharField(max_length=255)
    contact_person = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=20)
    clinic_group = models.CharField(max_length=255, blank=True, null=True)
    status = models.CharField(max_length=15, choices=Status.choices, default=Status.PENDING)
    join_network = models.BooleanField(default=False)
    privacy_and_terms_accepted = models.BooleanField(default=False)
    clinic_admin = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='managed_clinic')
    facility_license_number = models.CharField(max_length=100, blank=True, null=True)
    accreditation_authority = models.CharField(max_length=255, blank=True, null=True)
    medical_license_document = models.FileField(upload_to='clinic_licenses/', blank=True, null=True)
    compliance_confirmed = models.BooleanField(default=False)
    public_activation=models.BooleanField(default=False) 
    
    rejection_reason = models.TextField(blank=True, null=True)
    total_beds = models.PositiveIntegerField(default=0, blank=True, null=True)
    accepted_infectious=models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        db_table = 'user_clinic'
    def __str__(self):
        return f"{self.clinic_name} ({self.get_status_display()})"

class ClinicProfile(models.Model):
    clinic = models.OneToOneField(ClinicRegister, on_delete=models.CASCADE, related_name='profile')
    name = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    distance_from_city_center = models.TextField( blank=True,null=True,)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    per_treatment_price=models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    # total_beds = models.PositiveIntegerField(default=0, blank=True, null=True)

    class Meta:
        db_table = 'user_clinic_profile'
    def __str__(self):
        return f"Profile for {self.clinic.clinic_name}"
    def get_average_rating(self):
        avg = self.ratings.aggregate(Avg('rating'))['rating__avg']
        return round(avg,1) if avg else 0

# Clinic Images
class ClinicImage(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='images')
    image = models.FileField(upload_to='clinic/')
# Clinic Video
class ClinicInsurance(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='insurances')
    insurance_name = models.CharField(max_length=255)

# Clinic Treatment
class ClinicTreatment(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='treatments')
    treatment_name = models.CharField(max_length=255)
    treatment_code = models.CharField(max_length=50, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    duration = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return f"{self.treatment_name} ({self.treatment_code or 'No Code'})"

# Clinic Facility
class ClinicFacility(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='facilities')
    facility_name = models.CharField(max_length=255)

# Clinic Accepted Patients
class ClinicAcceptedPatients(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='accepted_patients')
    patient_name = models.CharField(max_length=255)

# Clinic Payment Method
class ClinicPaymentMethod(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='payment_methods')
    payment_method_name = models.CharField(max_length=255)

# Clinic Availability
class ClinicAvailability(models.Model):
    clinic = models.ForeignKey( ClinicProfile,on_delete=models.CASCADE,related_name='availabilities')
    date = models.DateField()
    # is_available = models.BooleanField(default=True)
    
# Clinic Rating
class ClinicRating(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)
    rating = models.DecimalField(max_digits=2, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        unique_together = ('clinic', 'user')
        db_table = 'user_clinicrating'