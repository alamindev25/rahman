import uuid
from django.db import models
from apps.clinic.models import ClinicProfile
from apps.user.models import User

# Clinic Appointment 
class ClinicAppointment(models.Model):
    STATUS_CHOICES =(
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
        ('completed', 'Completed'),
    )
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    clinic = models.ForeignKey(ClinicProfile,on_delete=models.CASCADE,null=True,blank=True)
    appointment_id = models.UUIDField(default=uuid.uuid4,unique=True,editable=False)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    total_price = models.DecimalField(max_digits=10,decimal_places=2,default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)
    
# Treatment Schedule
class TreatmentSchedule(models.Model):
    SHIFT_CHOICES = (
            ('morning','Morning shift'),
            ('afternoon','Afternoon shift'),
            ('evening','Evening shift'),
        )
    appointment = models.ForeignKey(ClinicAppointment,related_name="schedules",on_delete=models.CASCADE)
    treatment_date = models.DateField()
    shift = models.CharField(max_length=20,choices=SHIFT_CHOICES)

class ClinicSlotCapacity(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning shift'),
        ('afternoon', 'Afternoon shift'),
        ('evening', 'Evening shift'),
    )
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='slot_capacities')
    date = models.DateField()
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    max_limit = models.PositiveIntegerField(default=10) 
    class Meta:
        unique_together = ('clinic', 'date', 'shift')
    def __str__(self):
        return f"{self.clinic.name} - {self.date} ({self.shift}) [Max: {self.max_limit}]"





# Weekly Operational Schedule (Mon-Sun Open/Closed)
class ClinicWeeklySchedule(models.Model):
    DAY_CHOICES = (
        ('mon', 'Monday'),
        ('tue', 'Tuesday'),
        ('wed', 'Wednesday'),
        ('thu', 'Thursday'),
        ('fri', 'Friday'),
        ('sat', 'Saturday'),
        ('sun', 'Sunday'),
    )
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='weekly_schedules')
    day_of_week = models.CharField(max_length=10, choices=DAY_CHOICES)
    is_open = models.BooleanField(default=True)

    class Meta:
        unique_together = ('clinic', 'day_of_week')
        verbose_name = 'Clinic Weekly Schedule'
        verbose_name_plural = 'Clinic Weekly Schedules'

    def __str__(self):
        return f"{self.clinic.name} - {self.get_day_of_week_display()}: {'Open' if self.is_open else 'Closed'}"

# Shift Timings & Bed Capacities (Morning, Afternoon, Evening)
class ClinicShiftTiming(models.Model):
    SHIFT_CHOICES = (
        ('morning', 'Morning Shift'),
        ('afternoon', 'Afternoon Shift'),
        ('evening', 'Evening Shift'),
    )
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='shift_timings')
    shift = models.CharField(max_length=20, choices=SHIFT_CHOICES)
    is_enabled = models.BooleanField(default=True)
    start_time = models.TimeField(null=True, blank=True)
    end_time = models.TimeField(null=True, blank=True)
    capacity = models.PositiveIntegerField(default=6)

    class Meta:
        unique_together = ('clinic', 'shift')
        verbose_name = 'Clinic Shift Timing'
        verbose_name_plural = 'Clinic Shift Timings'

    def __str__(self):
        return f"{self.clinic.name} - {self.get_shift_display()} (Cap: {self.capacity})"

# Blackout & Maintenance Dates
class ClinicBlackoutDate(models.Model):
    clinic = models.ForeignKey(ClinicProfile, on_delete=models.CASCADE, related_name='blackout_dates')
    date = models.DateField()
    reason = models.CharField(max_length=255, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('clinic', 'date')
        ordering = ['date']
        verbose_name = 'Clinic Blackout Date'
        verbose_name_plural = 'Clinic Blackout Dates'

    def __str__(self):
        return f"{self.clinic.name} - {self.date} ({self.reason})"








# Patient Detail
class PatientDetail(models.Model):
    appointment = models.OneToOneField(ClinicAppointment,on_delete=models.CASCADE,related_name='patient_detail')
    full_name=models.CharField( max_length=200)
    email=models.EmailField( max_length=200)
    phone=models.CharField(max_length=20)
    birth_date=models.DateField()
    language=models.CharField(max_length=50,default="English")


# Patient Health Status
class PatientHealthStatus(models.Model):
    appointment =models.OneToOneField(ClinicAppointment,on_delete=models.CASCADE,related_name='health_status')
    hivpositive=models.BooleanField(default=False)
    hvbpositive=models.BooleanField(default=False)
    hcvpositive=models.BooleanField(default=False)

# Patient Insurance
class PatientInsurance(models.Model):
    appointment=models.OneToOneField(ClinicAppointment,on_delete=models.CASCADE,related_name='insurance')
    ehic_holder=models.BooleanField(default=False)
    ghic_holder=models.BooleanField(default=False)

# Patient Medical History
class TreatmentType(models.Model):
    TYPE_CHOICES=(
            ('HD','Dialysis HD'),
            ('HDF','Dialysis HDF'),
        )
    appointment=models.OneToOneField(ClinicAppointment,on_delete=models.CASCADE,related_name='treatment_type')
    treatment_type=models.CharField(max_length=10,choices=TYPE_CHOICES)
    
class CarePartner(models.Model):
    appointment=models.OneToOneField(ClinicAppointment,on_delete=models.CASCADE,related_name='care_partner')
    bringing_partner=models.BooleanField(default=False)

# Patient Home Clinic
class HomeClinic(models.Model):
    appointment=models.OneToOneField(ClinicAppointment, on_delete=models.CASCADE, related_name='home_clinic')
    clinic_name=models.CharField(max_length=200,blank=True)
    home_clinic_consultant_name=models.CharField(max_length=200,blank=True)
    
# Patient Medical Report
class MedicalReport(models.Model):
    appointment = models.ForeignKey(ClinicAppointment, on_delete=models.CASCADE, related_name='medical_reports')
    file = models.FileField(upload_to='medical_reports/')