from django.contrib import admin
from unfold.admin import ModelAdmin, TabularInline

# Register your models here.
from .models import (
    ClinicAppointment,  
    TreatmentSchedule,
    PatientDetail,
    PatientHealthStatus,
    PatientInsurance,
    TreatmentType,
    CarePartner,
    HomeClinic,
    MedicalReport,
    ClinicSlotCapacity,
    ClinicWeeklySchedule,
    ClinicShiftTiming,
    ClinicBlackoutDate,
)
class TreatmentScheduleInline(TabularInline):
    model = TreatmentSchedule
    extra = 1
    fields = ['treatment_date', 'shift']

@admin.register(ClinicAppointment)
class ClinicAppointmentAdmin(ModelAdmin):
    list_display = ['id', 'user', 'clinic', 'status', 'total_price', 'get_treatment_dates', 'get_shifts', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ('status',)
    search_fields = ['id', 'status']
    inlines = [TreatmentScheduleInline]

    @admin.display(description='Treatment Dates')
    def get_treatment_dates(self, obj):
        schedules = obj.schedules.all()
        if schedules.exists():
            return ", ".join([str(s.treatment_date) for s in schedules])
        return "-"
    @admin.display(description='Shifts')
    def get_shifts(self, obj):
        schedules = obj.schedules.all()
        if schedules.exists():
            return ", ".join([s.get_shift_display() for s in schedules])
        return "-"

@admin.register(ClinicSlotCapacity)
class ClinicSlotCapacityAdmin(ModelAdmin):
    list_display = ('clinic', 'date', 'shift', 'max_limit')
    list_filter = ('clinic', 'date', 'shift')
    list_editable = ('max_limit',)
    search_fields = ('clinic__name', 'date')
    
@admin.register(PatientDetail)
class PatientDetailAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'full_name', 'email', 'phone', 'birth_date', 'language']
    search_fields = ['appointment__id', 'full_name', 'email']
@admin.register(PatientHealthStatus)
class PatientHealthStatusAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'hivpositive', 'hvbpositive', 'hcvpositive']
    search_fields = ['appointment__id']

@admin.register(PatientInsurance)
class PatientInsuranceAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'ehic_holder', 'ghic_holder']
    search_fields = ['appointment__id']
@admin.register(TreatmentType)
class TreatmentTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'treatment_type']
    search_fields = ['appointment__id']

@admin.register(CarePartner)
class CarePartnerAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'bringing_partner']
    search_fields = ['appointment__id']
@admin.register(HomeClinic)
class HomeClinicAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'clinic_name', 'home_clinic_consultant_name']
    search_fields = ['appointment__id', 'clinic_name']

@admin.register(MedicalReport)
class MedicalReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'appointment', 'file']
    search_fields = ['appointment__id', 'file']

    

@admin.register(ClinicWeeklySchedule)
class ClinicWeeklyScheduleAdmin(ModelAdmin):
    list_display = ('clinic', 'day_of_week', 'is_open')
    list_filter = ('clinic', 'day_of_week', 'is_open')
    list_editable = ('is_open',)

@admin.register(ClinicShiftTiming)
class ClinicShiftTimingAdmin(ModelAdmin):
    list_display = ('clinic', 'shift', 'is_enabled', 'start_time', 'end_time', 'capacity')
    list_filter = ('clinic', 'shift', 'is_enabled')
    list_editable = ('is_enabled', 'capacity')

@admin.register(ClinicBlackoutDate)
class ClinicBlackoutDateAdmin(ModelAdmin):
    list_display = ('clinic', 'date', 'reason', 'created_at')
    list_filter = ('clinic', 'date')
    search_fields = ('clinic__name', 'reason')


