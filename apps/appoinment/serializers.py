import json
from decimal import Decimal
from rest_framework import request, serializers
from django.db import transaction
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from .models import(
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
from apps.clinic.models import ClinicTreatment

def get_clinic_treatment_price(clinic, treatment_type_str):
    
    """
    Find price from ClinicTreatment for the given clinic matching treatment_type_str.
    Supports matching 'HD'/'Dialysis HD' or 'HDF'/'Dialysis HDF'.
    """
    if not clinic or not treatment_type_str:
        return None
    t_str = str(treatment_type_str).strip()
    # Exact match first
    ct = ClinicTreatment.objects.filter(clinic=clinic, treatment_name__iexact=t_str).first()
    if ct:
        return ct.price
    # Match by key or substring (e.g., 'HD' -> 'Dialysis HD', 'HDF' -> 'Dialysis HDF')
    upper_t = t_str.upper()
    if upper_t in ['HD', 'HDF']:
        full_name = f"Dialysis {upper_t}"
        ct = ClinicTreatment.objects.filter(clinic=clinic, treatment_name__iexact=full_name).first()
        if ct:
            return ct.price
    if 'HDF' in upper_t:
        ct = ClinicTreatment.objects.filter(clinic=clinic, treatment_name__icontains='HDF').first()
        if ct:
            return ct.price
    elif 'HD' in upper_t:
        ct = ClinicTreatment.objects.filter(clinic=clinic, treatment_name__icontains='HD').first()
        if ct:
            return ct.price
    ct = ClinicTreatment.objects.filter(clinic=clinic).first()
    if ct:
        return ct.price
    return None

class TreatmentScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentSchedule
        fields = ['id','appointment','treatment_date','shift',]
        read_only_fields = ['appointment']

class PatientDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientDetail
        fields = ['id','appointment','full_name','email','phone','birth_date','language',]
        read_only_fields = ['appointment']

# PatientHealthStatus Serializer
class PatientHealthStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientHealthStatus
        fields = ['id','appointment','hivpositive','hvbpositive','hcvpositive',]
        read_only_fields = ['appointment']

# PatientInsurance Serializer
class PatientInsuranceSerializer(serializers.ModelSerializer):
    class Meta:
        model = PatientInsurance
        fields = ['id','appointment','ehic_holder','ghic_holder',]
        read_only_fields = ['appointment']

# TreatmentType Serializer
class TreatmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TreatmentType
        fields = ['id','appointment','treatment_type',]
        read_only_fields = ['appointment']

# CarePartner Serializer
class CarePartnerSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarePartner
        fields = ['id','appointment','bringing_partner',]
        read_only_fields = ['appointment']

# HomeClinic Serializer
class HomeClinicSerializer(serializers.ModelSerializer):
    class Meta:
        model = HomeClinic
        fields = ['id','appointment','clinic_name','home_clinic_consultant_name',]
        read_only_fields = ['appointment']

# MedicalReport Serializer
class MedicalReportSerializer(serializers.ModelSerializer):
    file= serializers.FileField(write_only=True)
    file_url = serializers.SerializerMethodField()
    class Meta:
        model = MedicalReport
        fields = ['id','appointment','file','file_url',]
        read_only_fields = ['appointment']
        extra_kwargs = {
            'file': {'write_only': True} # 
        }

    # Custom method to get the absolute URL of the file
    def get_file_url(self, obj):
        request = self.context.get('request')
        if obj.file and hasattr(obj.file, 'url'):
            file_url = obj.file.url
            if request is not None:
                return request.build_absolute_uri(file_url)
            return file_url
        return None


# ClinicAppointment Serializer
class ClinicAppointmentSerializer(serializers.ModelSerializer):
    schedules=TreatmentScheduleSerializer(many=True, required=False)
    patient_detail=PatientDetailSerializer(required=False,allow_null=True)
    health_status=PatientHealthStatusSerializer(required=False,allow_null=True)
    insurance=PatientInsuranceSerializer(required=False,allow_null=True)
    treatment_type=TreatmentTypeSerializer(required=False)
    care_partner=CarePartnerSerializer(required=False)
    home_clinic=HomeClinicSerializer(required=False)
    medical_reports=MedicalReportSerializer(many=True, required=False)

    # Formatted UI presentation fields matching the reference design
    formatted_booking_id = serializers.SerializerMethodField()
    patient = serializers.SerializerMethodField()
    treatment = serializers.SerializerMethodField()
    dates_and_shift = serializers.SerializerMethodField()
    serology_health = serializers.SerializerMethodField()
    status_display = serializers.SerializerMethodField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = ClinicAppointment
        fields = [
            'id',
            'user',
            'clinic',
            'appointment_id',
            'formatted_booking_id',
            'patient',
            'treatment',
            'dates_and_shift',
            'serology_health',
            'status',
            'status_display',
            'actions',
            'total_price',
            'created_at',
            'schedules',
            'patient_detail',
            'health_status',
            'insurance',
            'treatment_type',
            'care_partner',
            'home_clinic',
            'medical_reports',
        ]

    def get_formatted_booking_id(self, obj):
        if hasattr(obj, 'appointment_id') and obj.appointment_id:
            short_uuid = str(obj.appointment_id).replace('-', '')[:6].upper()
            return f"#MED-2026-{short_uuid}"
        return f"#MED-2026-{obj.id:03d}"

    def get_patient(self, obj):
        pd = getattr(obj, 'patient_detail', None)
        booking_id = self.get_formatted_booking_id(obj)
        if not pd:
            return {
                "full_name": "",
                "initial": "",
                "booking_id": booking_id,
                "phone": "",
                "email": ""
            }
        full_name = pd.full_name or ""
        initial = full_name[0].upper() if full_name else ""
        return {
            "full_name": full_name,
            "initial": initial,
            "booking_id": booking_id,
            "phone": pd.phone or "",
            "email": pd.email or ""
        }

    def get_treatment(self, obj):
        tt = getattr(obj, 'treatment_type', None)
        if not tt or not tt.treatment_type:
            return {"code": "HD", "name": "Dialysis HD"}
        t_code = tt.treatment_type
        t_name = tt.get_treatment_type_display() if hasattr(tt, 'get_treatment_type_display') else t_code
        return {
            "code": t_code,
            "name": t_name
        }

    def get_dates_and_shift(self, obj):
        schedules = list(obj.schedules.all()) if hasattr(obj, 'schedules') else []
        if not schedules:
            return {
                "formatted_date": "N/A",
                "formatted_shift": "N/A",
                "primary_date": None,
                "primary_shift": None,
                "total_schedules": 0
            }
        first_s = schedules[0]
        formatted_date = first_s.treatment_date.strftime("%b %d, %Y") if first_s.treatment_date else "N/A"
        shift_raw = first_s.shift or ""
        shift_display = first_s.get_shift_display() if hasattr(first_s, 'get_shift_display') else shift_raw.title()
        extra_count = len(schedules) - 1
        formatted_shift = f"{shift_display} (+{extra_count} More)" if extra_count > 0 else shift_display
        return {
            "formatted_date": formatted_date,
            "formatted_shift": formatted_shift,
            "primary_date": str(first_s.treatment_date) if first_s.treatment_date else None,
            "primary_shift": shift_raw,
            "total_schedules": len(schedules)
        }

    def get_serology_health(self, obj):
        hs = getattr(obj, 'health_status', None)
        if not hs:
            return {
                "label": "Standard",
                "is_isolation_required": False,
                "hivpositive": False,
                "hvbpositive": False,
                "hcvpositive": False
            }
        is_isolation = bool(hs.hivpositive or hs.hvbpositive or hs.hcvpositive)
        label = "Isolation Req." if is_isolation else "Standard"
        return {
            "label": label,
            "is_isolation_required": is_isolation,
            "hivpositive": bool(hs.hivpositive),
            "hvbpositive": bool(hs.hvbpositive),
            "hcvpositive": bool(hs.hcvpositive)
        }

    def get_status_display(self, obj):
        return obj.get_status_display() if hasattr(obj, 'get_status_display') else (obj.status or "").title()

    def get_actions(self, obj):
        status_val = (obj.status or "").lower()
        return {
            "can_view": True,
            "can_approve": status_val == 'pending',
            "can_reject": status_val == 'pending',
            "can_complete": status_val == 'confirmed',
            "can_cancel": status_val in ['pending', 'confirmed']
        }        
    def validate(self, attrs):
        clinic = attrs.get('clinic')
        schedules = attrs.get('schedules', [])
        if not schedules and 'request' in self.context:
            raw_s = self.context['request'].data.get('schedules')
            if isinstance(raw_s, str):
                try:
                    raw_s = json.loads(raw_s)
                except Exception:
                    raw_s = []
            if isinstance(raw_s, dict):
                schedules = [raw_s]
            elif isinstance(raw_s, list):
                schedules = raw_s

        if clinic and schedules:
            seen_slots = set()
            for schedule in schedules:
                if isinstance(schedule, str):
                    try:
                        schedule = json.loads(schedule)
                    except Exception:
                        continue
                if isinstance(schedule, dict):
                    t_date = schedule.get('treatment_date')
                    shift = schedule.get('shift')
                else:
                    t_date = getattr(schedule, 'treatment_date', None)
                    shift = getattr(schedule, 'shift', None)
                if t_date and shift:
                    t_date_str = str(t_date)
                    slot_key = (t_date_str, shift)
                    if slot_key in seen_slots:
                        raise serializers.ValidationError({
                            "schedules": f"Duplicate shift '{shift}' on date '{t_date_str}' in your request."
                        })
                    seen_slots.add(slot_key)
                    slot_config = ClinicSlotCapacity.objects.filter(
                        clinic=clinic,
                        date=t_date,
                        shift=shift
                    ).first()
                    if slot_config:
                        max_limit = slot_config.max_limit
                    else:
                        max_limit = getattr(clinic, 'default_slot_limit', 10)
                    booked_count = TreatmentSchedule.objects.filter(
                        appointment__clinic=clinic,
                        treatment_date=t_date,
                        shift=shift,
                        appointment__status__in=['pending', 'confirmed', 'completed']
                    ).count()
                    if booked_count >= max_limit:
                        raise serializers.ValidationError({
                            "schedules": f"The shift '{shift}' on date '{t_date_str}' is fully booked. Please choose another date or shift."
                        })
        return attrs

    @transaction.atomic
    def create(self, validated_data):
        request = self.context['request']
        def safe_dict(val):
            if isinstance(val, str):
                try:
                    val = json.loads(val)
                except Exception:
                    return {}
            return val if isinstance(val, dict) else {}
        
        def safe_list(val):
            if isinstance(val, str):
                try:
                    val = json.loads(val)
                except Exception:
                    return []
            if isinstance(val, dict):
                return [val]
            return val if isinstance(val, list) else []

        def get_field_data(field_name, is_list=False):
            val = validated_data.pop(field_name, None)
            if (val is None or val == [] or val == {}) and field_name in request.data:
                val = request.data.get(field_name)
            if is_list:
                return safe_list(val)
            return safe_dict(val)

        schedules_data = get_field_data('schedules', is_list=True)
        patient_data = get_field_data('patient_detail')
        health_data = get_field_data('health_status')
        insurance_data = get_field_data('insurance')
        treatment_data = get_field_data('treatment_type')
        care_partner_data = get_field_data('care_partner')
        home_clinic_data = get_field_data('home_clinic')
        medical_reports_data = validated_data.pop('medical_reports', [])

        appointment = ClinicAppointment.objects.create(
            user=self.context['request'].user,
            **validated_data
        )
        # Treatment Schedule Create
        for schedule in schedules_data:
            if isinstance(schedule, str):
                try:
                    schedule = json.loads(schedule)
                except Exception:
                    continue
            if isinstance(schedule, dict):
                TreatmentSchedule.objects.create(
                    appointment=appointment,
                    **schedule
                )
        # Patient Details
        if patient_data:
            PatientDetail.objects.create(
                appointment=appointment,
                **patient_data
            )
        # Health Status
        if health_data:
            PatientHealthStatus.objects.create(
                appointment=appointment,
                **health_data
            )
        # Insurance
        if insurance_data:
            PatientInsurance.objects.create(
                appointment=appointment,
                **insurance_data
            )

        # Treatment Type
        if treatment_data:
            TreatmentType.objects.create(
                appointment=appointment,
                **treatment_data
            )

        # Care Partner
        if care_partner_data:
            CarePartner.objects.create(
                appointment=appointment,
                **care_partner_data
            )
        # Home Clinic
        if home_clinic_data:
            HomeClinic.objects.create(
                appointment=appointment,
                **home_clinic_data
            )
        if request.FILES:
            files = request.FILES.getlist('medical_reports')
            for file in files:
                MedicalReport.objects.create(
                    appointment=appointment,
                    file=file
                )
        # Auto-calculate total_price based on selected treatment price * number of schedules
        if ('total_price' not in validated_data or not validated_data['total_price'] or validated_data['total_price'] == 0) and appointment.clinic:
            treatment_type_val = treatment_data.get('treatment_type') if treatment_data else None
            unit_price = get_clinic_treatment_price(appointment.clinic, treatment_type_val)
            if unit_price is None or unit_price <= 0:
                unit_price = getattr(appointment.clinic, 'per_treatment_price', 0) or Decimal('0.00')

            schedule_count = Decimal(str(max(len(schedules_data), 1)))
            appointment.total_price = Decimal(str(unit_price)) * schedule_count
            appointment.save()

        # Reload related objects
        appointment.refresh_from_db()
        appointment = ClinicAppointment.objects.prefetch_related('schedules','medical_reports').select_related(
              'patient_detail',
              'health_status',
              'insurance',
              'treatment_type',
              'care_partner',
              'home_clinic'
            ).get(
                id=appointment.id
       )
        return appointment

class BookingHistorySerializer(serializers.ModelSerializer):
    clinic_name = serializers.SerializerMethodField()
    clinic_image = serializers.SerializerMethodField()
    location = serializers.SerializerMethodField() 
    treatment_type = serializers.SerializerMethodField()
    treatment_dates = serializers.SerializerMethodField()
    selected_shift = serializers.SerializerMethodField()
    receipt_url = serializers.SerializerMethodField()
    can_review = serializers.SerializerMethodField()
    is_reviewed = serializers.SerializerMethodField()

    class Meta:
        model = ClinicAppointment
        fields = [
            'id',
            'appointment_id',
            'clinic_name',
            'clinic_image',
            'location',
            'status',
            'total_price', 
            'treatment_type',
            'treatment_dates',
            'selected_shift',
            'receipt_url',
            'can_review',
            'is_reviewed',
            'created_at',
        ]

    def get_clinic_name(self, obj):
        if obj.clinic:
            return obj.clinic.name or (obj.clinic.clinic.clinic_name if getattr(obj.clinic, 'clinic', None) else None)
        return None

    def get_clinic_image(self, obj):
        request = self.context.get('request')
        if obj.clinic:
            if hasattr(obj.clinic, 'image') and obj.clinic.image:
                image_url = obj.clinic.image.url
                return request.build_absolute_uri(image_url) if request else image_url
            first_image = obj.clinic.images.first() if hasattr(obj.clinic, 'images') else None
            if first_image and first_image.image:
                image_url = first_image.image.url
                return request.build_absolute_uri(image_url) if request else image_url
        return None

    def get_location(self, obj):
        if not obj.clinic:
            return None
        return {
            "country": obj.clinic.country,
            "city": obj.clinic.city,
            "address": obj.clinic.address,
            "latitude": obj.clinic.latitude,
            "longitude": obj.clinic.longitude,
        }

    def get_treatment_type(self, obj):
        if hasattr(obj, 'treatment_type') and obj.treatment_type:
            return obj.treatment_type.get_treatment_type_display()
        return None

    def get_treatment_dates(self, obj):
        schedules = obj.schedules.all()
        if not schedules.exists():
            return None
        dates = [str(s.treatment_date) for s in schedules]
        if len(dates) == 1:
            return dates[0]
        return f"{dates[0]} - {dates[-1]}"

    def get_selected_shift(self, obj):
        schedule = obj.schedules.first()
        if schedule:
            return schedule.get_shift_display()
        return None

    def get_receipt_url(self, obj):
        request = self.context.get('request')
        report = obj.medical_reports.first()
        if report and report.file:
            return request.build_absolute_uri(report.file.url) if request else report.file.url
        if request:
            return request.build_absolute_uri(f"/api/appointments/{obj.id}/receipt/")
        return f"/api/appointments/{obj.id}/receipt/"

    def get_can_review(self, obj):
        return obj.status in ['completed', 'confirmed']

    def get_is_reviewed(self, obj):
        if obj.clinic and obj.user:
            from apps.clinic.models import ClinicRating
            return ClinicRating.objects.filter(clinic=obj.clinic, user=obj.user).exists()
        return False


class ClinicSlotCapacitySerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicSlotCapacity
        fields = ['id', 'clinic', 'date', 'shift', 'max_limit']

class ClinicSlotCheckingSerializer(serializers.ModelSerializer):
    treatment_date = serializers.DateField(write_only=True)
    shift = serializers.CharField(max_length=20, write_only=True)
    max_limit = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = ClinicAppointment
        fields = ['id', 'clinic', 'total_price', 'max_limit', 'treatment_date', 'shift', 'status', 'appointment_id']
        read_only_fields = ['appointment_id', 'status', 'max_limit']

    def get_max_limit(self, obj):
        schedule = obj.schedules.first()
        if not schedule:
            return 10   
        slot_config = ClinicSlotCapacity.objects.filter(
            clinic=obj.clinic, 
            date=schedule.treatment_date, 
            shift=schedule.shift
        ).first()
        if slot_config:
            return slot_config.max_limit
        return getattr(obj.clinic, 'default_slot_limit', 10)

    def create(self, validated_data):
        date = validated_data.pop('treatment_date')
        shift = validated_data.pop('shift')
        clinic = validated_data['clinic']
        slot_config = ClinicSlotCapacity.objects.filter(
            clinic=clinic, 
            date=date, 
            shift=shift
        ).first()
        if slot_config:
            max_limit = slot_config.max_limit
        else:
            max_limit = getattr(clinic, 'default_slot_limit', 10)
        current_bookings_count = TreatmentSchedule.objects.filter(
            appointment__clinic=clinic,
            treatment_date=date,
            shift=shift,
            appointment__status__in=['pending', 'confirmed', 'completed']
        ).count()
        if current_bookings_count >= max_limit:
            raise ValidationError({"error": "This slot is fully booked. Please choose another date or shift."})
        appointment = ClinicAppointment.objects.create(**validated_data)
        if ('total_price' not in validated_data or not validated_data['total_price']) and clinic:
            per_price = getattr(clinic, 'per_treatment_price', 0) or 0
            appointment.total_price = per_price
            appointment.save()
        TreatmentSchedule.objects.create(
            appointment=appointment,
            treatment_date=date,
            shift=shift
        )
        return appointment

class AppointmentStatusUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicAppointment
        fields = ['id', 'status', 'total_price']
        extra_kwargs = {
            'status': {'required': True}
        }
    def validate_status(self, value):
        valid_statuses = [choice[0] for choice in ClinicAppointment.STATUS_CHOICES]
        if value not in valid_statuses:
            raise serializers.ValidationError(
                f"Invalid status '{value}'. Allowed values are: {', '.join(valid_statuses)}"
            )
        return value



        


class ClinicWeeklyScheduleSerializer(serializers.ModelSerializer):
    day_name = serializers.CharField(source='get_day_of_week_display', read_only=True)
    class Meta:
        model = ClinicWeeklySchedule
        fields = ['id', 'clinic', 'day_of_week', 'day_name', 'is_open']
        extra_kwargs = {'clinic': {'required': False}}


class ClinicShiftTimingSerializer(serializers.ModelSerializer):
    shift_name = serializers.CharField(source='get_shift_display', read_only=True)
    class Meta:
        model = ClinicShiftTiming
        fields = ['id', 'clinic', 'shift', 'shift_name', 'is_enabled', 'start_time', 'end_time', 'capacity']
        extra_kwargs = {'clinic': {'required': False}}


class ClinicBlackoutDateSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClinicBlackoutDate
        fields = ['id', 'clinic', 'date', 'reason', 'created_at']
        extra_kwargs = {'clinic': {'required': False}}


