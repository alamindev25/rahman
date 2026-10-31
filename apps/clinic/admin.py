from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin
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
@admin.register(ClinicRegister)
class ClinicRegisterAdmin(ModelAdmin):
    list_display = ('id', 'clinic_name', 'contact_person', 'email', 'phone_number', 'status', 'clinic_admin')
    list_display_links = ('id', 'clinic_name')
    list_filter = ('status', 'created_at')
    list_editable = ('status',)
    search_fields = ('clinic_name', 'contact_person', 'email', 'phone_number')
    readonly_fields = ('clinic_admin', 'created_at', 'updated_at')
    fieldsets = (
        (_('Clinic Core Identity'), {
            'fields': ('clinic_name', 'clinic_group', 'contact_person')
        }),
        (_('Communication Protocols'), {
            'fields': ('email', 'phone_number')
        }),
        (_('System Multi-Tenant Scope & Action Control'), {
            'description': _('Change validation status from <b>Pending</b> to <b>Approved</b> to auto-generate secure login tokens dynamically.'),
            'fields': ('status', 'clinic_admin',  )
        }),
    )
#New add
    def save_model(self, request, obj, form, change):
        old_status = None
        if change and obj.pk:
            old_obj = ClinicRegister.objects.filter(pk=obj.pk).first()
            if old_obj:
                old_status = old_obj.status

        super().save_model(request, obj, form, change)

        if change and old_status != obj.status:
            from .utils import send_clinic_approved_email, send_clinic_rejected_email
            if obj.status == ClinicRegister.Status.APPROVED:
                send_clinic_approved_email(obj)
            elif obj.status == ClinicRegister.Status.REJECTED:
                send_clinic_rejected_email(obj, reason=getattr(obj, 'rejection_reason', None))

@admin.register(ClinicProfile)
class ClinicProfileAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'country',
        'city',
        'per_treatment_price',
    )
    search_fields = (
        'clinic__clinic_name',
        'country',
        'city',
    )
@admin.register(ClinicImage)
class ClinicImageAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'image',
    )
    search_fields = (
        'clinic__clinic__clinic_name',
    )
@admin.register(ClinicInsurance)
class ClinicInsuranceAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'insurance_name',
    )
    search_fields = (
        'insurance_name',
    )

@admin.register(ClinicTreatment)
class ClinicTreatmentAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'treatment_name',
        'treatment_code',
        'price',
        'duration',
    )
    search_fields = (
        'treatment_name',
        'treatment_code',
    )


@admin.register(ClinicFacility)
class ClinicFacilityAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'facility_name',
    )
    search_fields = (
        'facility_name',
    )

@admin.register(ClinicAcceptedPatients)
class ClinicAcceptedPatientsAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'patient_name',
    )
    search_fields = (
        'patient_name',
    )
@admin.register(ClinicPaymentMethod)
class ClinicPaymentMethodAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'payment_method_name',
    )
    search_fields = (
        'payment_method_name',
    )
@admin.register(ClinicAvailability)
class ClinicAvailabilityAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'date',
        # 'is_available',
    )
    list_filter = (
        # 'is_available',
        'date',
    )

@admin.register(ClinicRating)
class ClinicRatingAdmin(ModelAdmin):
    list_display = (
        'id',
        'clinic',
        'user',
        'rating',
        'created_at',
    )
    list_filter = (
        'rating',
        'created_at',
    )
    search_fields = (
        'clinic__clinic_name',
        'user__email',
    )

# @admin.register(ClinicRating)
# class ClinicRatingAdmin(ModelAdmin):
#     list_display = ('id', 'clinic', 'user', 'rating', 'created_at')
#     list_filter = ('created_at',)
#     search_fields = ('clinic__clinic_name', 'user__email')
