from rest_framework import generics, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import ClinicRegister, ClinicProfile, ClinicTreatment
from .serializers import (
    ClinicGetProfileSerializer,
    ClinicRatingSerializer,
    ClinicRegisterSerializer,
    ClinicProfileSerializer,
    ClinicSubmissionStatusSerializer,
    ClinicTreatmentSerializer,
)
from apps.utils.helpers import success, error
from apps.clinic.utils import send_clinic_pending_email, send_admin_clinic_request_email
from .utils import send_clinic_approved_email, send_clinic_rejected_email
from django.db.models import Avg
from django.db.models import Q
from apps.appoinment.models import ClinicSlotCapacity, TreatmentSchedule, ClinicAppointment, PatientDetail, PatientHealthStatus, TreatmentType
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
import json

# Clinic Registration
class ClinicRegisterView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def get_user_clinic(self, user):
        return ClinicRegister.objects.filter(
            Q(owner=user) | Q(clinic_admin=user)
        ).first()
    def get(self, request):
        user_clinic = self.get_user_clinic(request.user)
        if user_clinic:
            serializer = ClinicRegisterSerializer(user_clinic, context={'request': request})
            status_serializer = ClinicSubmissionStatusSerializer(user_clinic, context={'request': request})
            return success(
                data={
                    "clinic": serializer.data,
                    "submission_status": status_serializer.data
                },
                message="Clinic registration details retrieved successfully.",
                status_code=status.HTTP_200_OK
            )
        clinics = ClinicRegister.objects.all()
        serializer = ClinicRegisterSerializer(clinics, many=True, context={'request': request})
        return success(data={"clinics": serializer.data}, message="Registered clinics list retrieved successfully.", status_code=status.HTTP_200_OK)

    def post(self, request):
        serializer = ClinicRegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            clinic = serializer.save()
            try:
                send_clinic_pending_email(clinic)
                send_admin_clinic_request_email(clinic)
            except Exception:
                pass
            return success(data={"register": serializer.data}, message="Clinic registered successfully. Waiting for admin approval.", status_code=status.HTTP_201_CREATED)
        return error(message="Clinic registration failed.", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def patch(self, request):
        clinic = self.get_user_clinic(request.user)
        if not clinic:
            return error(message="No registered clinic found for this user.", status_code=status.HTTP_404_NOT_FOUND)

        serializer = ClinicRegisterSerializer(
            clinic,
            data=request.data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return success(data={"clinic": serializer.data}, message="Clinic registration details updated successfully.", status_code=status.HTTP_200_OK)
        return error(message="Failed to update clinic registration details.", errors=serializer.errors, status_code=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        return self.patch(request)


# Clinic Submission Status Overview API (GET endpoint for application submission/review status screen)
class ClinicSubmissionStatusAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get_user_clinic(self, user):
        return ClinicRegister.objects.filter(
            Q(owner=user) | Q(clinic_admin=user)
        ).first()

    def get(self, request):
        clinic = self.get_user_clinic(request.user)
        if not clinic:
            return success(
                data={"submission_status": None},
                message="No clinic registration found for this user.",
                status_code=status.HTTP_200_OK
            )
        serializer = ClinicSubmissionStatusSerializer(clinic, context={'request': request})
        return success(
            data={"submission_status": serializer.data},
            message="Clinic submission status retrieved successfully.",
            status_code=status.HTTP_200_OK
        )

# Admin Clinic Approval
class AdminClinicApproveView(APIView):
    permission_classes=[ AllowAny]
    def patch(self, request, pk):
        clinic = ClinicRegister.objects.get(id=pk)
        if clinic.status == ClinicRegister.Status.APPROVED:
            return Response(
                {
                    "message":
                    "Already approved."
                }
            )
        clinic.status = (ClinicRegister.Status.APPROVED)
        clinic.save()
        send_clinic_approved_email(clinic)
        return Response(
            {
                "message":
                "Clinic approved successfully."
            }
        )
    def get(self, request, pk):
        return self.patch(request, pk)


class AdminClinicRejectView(APIView):
    permission_classes=[
    AllowAny
    ]
    def patch(self, request, pk):
        clinic = ClinicRegister.objects.get(id=pk)
        reason = request.data.get("reason")
        clinic.status = (ClinicRegister.Status.REJECTED)
        clinic.rejection_reason = reason
        clinic.save()
        send_clinic_rejected_email(clinic,reason )
        return Response(
            {
                "message":
                "Clinic rejected successfully."
            }
        )

# Email-based Clinic Approval
class EmailApproveClinicView(APIView):
    def get(self, request, token):
        clinic = ClinicRegister.objects.get(approval_token=token)
        clinic.status = (ClinicRegister.Status.APPROVED)
        clinic.save()
        send_clinic_approved_email(clinic)
        return Response(
            {
                "message":
                "Clinic approved."
            }
        )
# Email-based Clinic Rejection
class EmailRejectClinicView(APIView):
    def post(self, request, token):
        clinic = ClinicRegister.objects.get( approval_token=token)
        reason = request.data.get("reason")
        clinic.status = (ClinicRegister.Status.REJECTED )
        clinic.rejection_reason = reason
        clinic.save()
        send_clinic_rejected_email( clinic,reason)
        return Response(
            {
                "message":
                "Clinic rejected."
            }
        )
# Clinic List View
class ClinicListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        clinics = ClinicProfile.objects.all()
        treatment_name = request.query_params.get("treatment", None)
        if treatment_name and treatment_name.lower() != 'all':
            clinics = clinics.filter(treatments__treatment_name__iexact=treatment_name).distinct()
        sort = request.query_params.get("sort", "price")
        if sort == "price":
            clinics = clinics.order_by("per_treatment_price")
        elif sort == "rating":
            clinics = clinics.annotate(
                average_rating=Avg("ratings__rating")
            ).order_by("-average_rating")
        elif sort == "distance":
            clinics = clinics.order_by(
                "distance_from_city_center"
            )
        else:
            return error(
                message="Invalid sorting option.",
                errors={
                    "sort": "Allowed values are: price, rating, distance."
                },
                status_code=status.HTTP_400_BAD_REQUEST
            )
        serializer = ClinicGetProfileSerializer(clinics,many=True, context={'request': request})
        return success(data={"clinics": serializer.data}, message="Clinic list retrieved successfully.", status_code=status.HTTP_200_OK)


# Treatment List GET API (Logged-in Clinic Owner/Admin only)
class ClinicTreatmentListAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get_user_clinic(self, user):
        return ClinicRegister.objects.filter(
            Q(owner=user) | Q(clinic_admin=user)
        ).first()

    def get(self, request):
        user_clinic = self.get_user_clinic(request.user)
        if not user_clinic or not hasattr(user_clinic, 'profile') or not user_clinic.profile:
            return error(
                message="Clinic profile not found for this user.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        treatments = ClinicTreatment.objects.filter(clinic=user_clinic.profile)
        treatment_name = request.query_params.get("treatment_name") or request.query_params.get("search")
        if treatment_name:
            treatments = treatments.filter(treatment_name__icontains=treatment_name)
        serializer = ClinicTreatmentSerializer(treatments, many=True, context={'request': request})
        return success(
            data={"treatments": serializer.data},
            message="Own clinic treatments retrieved successfully.",
            status_code=status.HTTP_200_OK
        )


# Clinic Profile Manage API (for logged in Clinic Owner: GET, POST, PUT, PATCH, DELETE)
class ClinicProfileCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser,FormParser,JSONParser]

    def get_user_clinic(self, user):
        return ClinicRegister.objects.filter(
            Q(owner=user) | Q(clinic_admin=user)
        ).first()

    def get(self, request):
        clinic = self.get_user_clinic(request.user)
        if not clinic or not hasattr(clinic, 'profile') or not clinic.profile:
            return error(
                message="Clinic profile not found for this user.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        serializer = ClinicProfileSerializer(clinic.profile, context={'request': request})
        return success(
            data={"clinic": serializer.data},
            message="Clinic profile retrieved successfully.",
            status_code=status.HTTP_200_OK
        )
    def post(self, request):
        user = request.user
        clinic = self.get_user_clinic(user)
        if not clinic:
            return error(
                message="No registered clinic found for this user. Please register a clinic first.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if hasattr(clinic, 'profile') and clinic.profile:
            return error(
                message="Clinic profile already exists for this clinic. Use PUT/PATCH to update.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
    def get_parsed_data(self, request):
        if hasattr(request.data, 'getlist'):
            data = {}
            for key in request.data.keys():
                if key in ['availabilities', 'treatments', 'facilities', 'insurances', 'accepted_patients', 'payment_methods', 'accepted_infectious', 'accepted_patient_categories', 'accepted_patients[]', 'accepted_infectious[]']:
                    list_val = request.data.getlist(key)
                    data[key] = list_val if len(list_val) > 1 else (list_val[0] if list_val else [])
                else:
                    data[key] = request.data[key]
        elif hasattr(request.data, 'dict'):
            data = request.data.dict()
        else:
            data = request.data.copy()

        nested_fields = ['availabilities', 'treatments', 'facilities', 'insurances', 'accepted_patients', 'payment_methods', 'accepted_infectious', 'accepted_patient_categories']
        for field in nested_fields:
            if field in data and isinstance(data[field], str):
                val = data[field].strip()
                if (val.startswith('{') and val.endswith('}')) or (val.startswith('[') and val.endswith(']')):
                    try:
                        data[field] = json.loads(val)
                    except json.JSONDecodeError:
                        pass
                elif ',' in val:
                    data[field] = [x.strip() for x in val.split(',') if x.strip()]

        if 'accepted_infectious' in data and ('accepted_patients' not in data or not data['accepted_patients']):
            data['accepted_patients'] = data['accepted_infectious']
        elif 'accepted_patients' in data and ('accepted_infectious' not in data or not data['accepted_infectious']):
            data['accepted_infectious'] = data['accepted_patients']

        return data
    def post(self, request):
        user = request.user
        clinic = self.get_user_clinic(user)
        if not clinic:
            return error(
                message="No registered clinic found for this user. Please register a clinic first.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        if hasattr(clinic, 'profile') and clinic.profile:
            return error(
                message="Clinic profile already exists for this clinic. Use PUT/PATCH to update.",
                status_code=status.HTTP_400_BAD_REQUEST
            )
        data = self.get_parsed_data(request)
        serializer = ClinicProfileSerializer(data=data, context={'request': request})
        if serializer.is_valid():
            serializer.save(clinic=clinic)
            return success(
                data={"clinic": serializer.data},
                message="Clinic profile created successfully.",
                status_code=status.HTTP_201_CREATED
            )
        return error(
            message="Failed to create clinic profile.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )
    def patch(self, request):
        clinic = self.get_user_clinic(request.user)

        if not clinic or not hasattr(clinic, 'profile') or not clinic.profile:
            return error(
                message="Clinic profile not found for this user.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        data = self.get_parsed_data(request)
        serializer = ClinicProfileSerializer(
            clinic.profile,
            data=data,
            partial=True,
            context={'request': request}
        )
        if serializer.is_valid():
            serializer.save()
            return success(
                data={"clinic": serializer.data},
                message="Clinic profile updated successfully.",
                status_code=status.HTTP_200_OK
            )
        return error(
            message="Failed to update clinic profile.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )

    def put(self, request):
        return self.patch(request)

    def delete(self, request):
        clinic= self.get_user_clinic(request.user)

        if not clinic or not hasattr(clinic, 'profile') or not clinic.profile:
            return error(
                message="Clinic profile not found for this user.",
                status_code=status.HTTP_404_NOT_FOUND
            )
        clinic.profile.delete()
        return success(
            message="Clinic profile deleted successfully.",
            status_code=status.HTTP_200_OK
        )

# Clinic Detail View (Public GET by PK)
class ClinicDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return ClinicProfile.objects.get(id=pk)
        except ClinicProfile.DoesNotExist:
            return None

    def get(self, request, pk):
        clinic = self.get_object(pk)
        if not clinic:
            return error(message="Clinic profile not found", status_code=status.HTTP_404_NOT_FOUND)
        serializer = ClinicProfileSerializer(clinic, context={'request': request})
        return success(data={"clinic": serializer.data}, message="Clinic details retrieved successfully.", status_code=status.HTTP_200_OK)

# Create Clinic Rating View
class CreateClinicRatingView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = ClinicRatingSerializer(
            data=request.data,
            context={"request": request}
        )
        if serializer.is_valid():
            user = request.user if request.user.is_authenticated else None
            serializer.save(user=user)
            return success(data={"rating": serializer.data}, message="Rating submitted successfully.", status_code=status.HTTP_201_CREATED)
        # return error(error=serializer.errors, message="Failed to submit rating.", status_code=status.HTTP_400_BAD_REQUEST)
        return error(message="Failed to submit rating.",errors=serializer.errors,status_code=status.HTTP_400_BAD_REQUEST)

class ClinicAdminDashboardListView(generics.ListAPIView):
    #serializer_class = ClinicAppointmentSerializer
    permission_classes = [permissions.IsAuthenticated]
    # def get_queryset(self):
    #     user = self.request.user
    #     # Security Guardrail Check 1: User level authentication check
    #     if user.role !='clinic_admin':
    #         raise PermissionDenied("Access denied. Only registered clinic administrators are allowed here.")
    #     try:
    #         assigned_clinic = user.clinic_profile
    #     except AttributeError:
    #         raise PermissionDenied("Configuration anomaly: No valid profile associated with this account.")
            
        # Strictly dynamic return constraints (Data row level security isolation mapping)
        # return Appointment.objects.filter(clinic=assigned_clinic).select_related('patient', 'patient__user_profile')

    def get(self, request):
        user = request.user
        clinic_id = request.query_params.get("clinic_id")
        if clinic_id:
            clinic_profile = ClinicProfile.objects.filter(id=clinic_id).first()
        else:
            clinic_reg = ClinicRegister.objects.filter(
                Q(owner=user) | Q(clinic_admin=user)
            ).first()
            clinic_profile = getattr(clinic_reg, 'profile', None) if clinic_reg else None

        if not clinic_profile:
            return error(
                message="No clinic profile found for this user.",
                status_code=status.HTTP_404_NOT_FOUND
            )

        # 1. Total appointments count
        total_appointments = ClinicAppointment.objects.filter(clinic=clinic_profile).count()
        # 2. Pending approval appointments count
        pending_approval = ClinicAppointment.objects.filter(
            clinic=clinic_profile, status='pending'
        ).count()
        # Additional statuses
        confirmed_appointments = ClinicAppointment.objects.filter(
            clinic=clinic_profile, status='confirmed'
        ).count()
        completed_appointments = ClinicAppointment.objects.filter(
            clinic=clinic_profile, status='completed'
        ).count()
        cancelled_appointments = ClinicAppointment.objects.filter(
            clinic=clinic_profile, status='cancelled'
        ).count()
        # 3. Booked slots count
        booked_slots = TreatmentSchedule.objects.filter(
            appointment__clinic=clinic_profile,
            appointment__status__in=['pending', 'confirmed']
        ).count()
        treatments = ClinicTreatment.objects.filter(clinic=clinic_profile).count()
        dashboard_data = {
            "clinic_id": clinic_profile.id,
            "clinic_name": getattr(clinic_profile, 'name', None) or getattr(clinic_profile.clinic, 'clinic_name', 'Clinic'),
            "overview": {
                "appointments": total_appointments,
                "pending_approval": pending_approval,
                "booked_slots": booked_slots,
                "treatments": treatments
            },
            "appointment_statuses": {
                "pending": pending_approval,
                "confirmed": confirmed_appointments,
                "completed": completed_appointments,
                "cancelled": cancelled_appointments
            }
        }
        return success(
            data=dashboard_data,
            message="Clinic owner dashboard overview retrieved successfully.",
            status_code=status.HTTP_200_OK
        )

class ClinicLocationDateSearchAPIView(APIView):
    permission_classes = [permissions.AllowAny] 
    def get(self, request):
        location_query = request.GET.get('location', '').strip()
        date_query = request.GET.get('date', '').strip()
        if not location_query or not date_query:
            return Response(
                {"error": "Both 'location' and 'date' query parameters are required."}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        clinics = ClinicProfile.objects.filter(
            Q(city__icontains=location_query) | 
            Q(country__icontains=location_query) |
            Q(address__icontains=location_query) |
            Q(name__icontains=location_query) |
            Q(clinic__clinic_name__icontains=location_query)
        ).distinct()
        
        if not clinics.exists():
            return Response({
                "location": location_query,
                "date": date_query,
                "count": 0,
                "clinics": []
            }, status=status.HTTP_200_OK)

        clinic_results = []
        for clinic in clinics:
            slot_capacities = ClinicSlotCapacity.objects.filter(
                clinic=clinic,
                date=date_query
            )
            shifts_data = []
            for slot in slot_capacities:
                booked_count = TreatmentSchedule.objects.filter(
                    appointment__clinic=clinic,
                    treatment_date=date_query,
                    shift=slot.shift,
                    appointment__status__in=['pending', 'confirmed']
                ).count()

                max_limit = slot.max_limit
                available_slots = max_limit - booked_count
                if available_slots < 0:
                    available_slots = 0
                shifts_data.append({
                    "shift": slot.shift,
                    "shift_display": slot.get_shift_display(),
                    "max_limit": max_limit,
                    "booked_count": booked_count,
                    "available_slots": available_slots,
                    "is_full": booked_count >= max_limit
                })
            if shifts_data:
                clinic_results.append({
                    "clinic_id": clinic.id,
                    "clinic_name": getattr(clinic, 'name', None) or getattr(clinic.clinic, 'clinic_name', 'Clinic'),
                    "address": getattr(clinic, 'address', ''),
                    "country": getattr(clinic, 'country', ''),
                    "city": getattr(clinic, 'city', ''),
                    "available_shifts": shifts_data
                })

        return Response({
            "location": location_query,
            "date": date_query,
            "count": len(clinic_results),
            "clinics": clinic_results
        }, status=status.HTTP_200_OK)


class HealthcareNetworkStatsAPIView(APIView):
  permission_classes = [permissions.AllowAny]
  def get(self, request):
    countries_count = (
        ClinicProfile.objects.exclude(country__isnull=True)
        .exclude(country="")
        .values("country")
        .distinct()
        .count()
    )
    centers_count = ClinicProfile.objects.count()
    bookings_count = TreatmentSchedule.objects.filter(
    appointment__status__in=["confirmed", "completed"]
    ).count()
    data = {
        "title": "Become Part of Our Healthcare Network",
        "subtitle": "Showcase your clinic and help patients find the care they need",
        "countries": {
            "count": countries_count,
            "display": f"{countries_count}+",
            "label": "Countries",
        },
        "centers": {
            "count": centers_count,
            "display": f"{centers_count}+",
            "label": "Dialysis Care Centers", 
        },
        "bookings": {
            "count": bookings_count,
            "display": (
                f"{bookings_count:,}+" if bookings_count > 0 else "0+"
            ),
            "label": "Booking Complete", 
        },
    }
    return Response(data, status=status.HTTP_200_OK)


class ClinicOwnerSignUpView(APIView):
    permission_classes = [AllowAny]
    parser_classes = [MultiPartParser, FormParser, JSONParser]

    def post(self, request):
        serializer = ClinicOwnerSignUpSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return success(
                data=serializer.data,
                message="Clinic Owner account registered successfully. Please verify your OTP.",
                status_code=status.HTTP_201_CREATED
            )
        return error(
            message="Clinic Owner registration failed.",
            errors=serializer.errors,
            status_code=status.HTTP_400_BAD_REQUEST
        )


#new Add 


class ClinicPartnerAppointmentsAPIView(APIView):
    permission_classes = [IsAuthenticated]
    def get_user_clinic_profiles(self, user):
        clinic_regs = ClinicRegister.objects.filter(
            Q(owner=user) | Q(clinic_admin=user)
        )
        profiles = ClinicProfile.objects.filter(clinic__in=clinic_regs)
        if profiles.exists():
            return profiles
        return ClinicProfile.objects.filter(clinic__owner=user)

    def get(self, request):
        clinic_profiles = self.get_user_clinic_profiles(request.user)
        if not clinic_profiles.exists():
            return error(message="No clinic profile found for this user.", status_code=status.HTTP_404_NOT_FOUND)

        queryset = ClinicAppointment.objects.filter(clinic__in=clinic_profiles).select_related(
            'patient_detail', 'health_status', 'treatment_type', 'user'
        ).prefetch_related('schedules').order_by('-created_at')
        total_count = queryset.count()
        pending_count = queryset.filter(status='pending').count()
        confirmed_count = queryset.filter(status='confirmed').count()
        completed_count = queryset.filter(status='completed').count()
        cancelled_count = queryset.filter(status='cancelled').count()
        status_param = request.GET.get('status', 'all').lower()
        if status_param and status_param != 'all':
            queryset = queryset.filter(status=status_param)
        search_query = request.GET.get('search', '').strip()
        if search_query:
            queryset = queryset.filter(
                Q(patient_detail__full_name__icontains=search_query) |
                Q(patient_detail__email__icontains=search_query) |
                Q(patient_detail__phone__icontains=search_query) |
                Q(appointment_id__icontains=search_query)
            )
        data = []
        for appt in queryset:
            p_detail = getattr(appt, 'patient_detail', None)
            health = getattr(appt, 'health_status', None)
            t_type = getattr(appt, 'treatment_type', None)
            schedules = list(appt.schedules.all())
            booking_id = f"#MED-2026-{appt.id}"
            is_isolation = False
            if health:
                is_isolation = bool(health.hivpositive or health.hvbpositive or health.hcvpositive)
            serology_status = "Isolation Req." if is_isolation else "Standard"
            treatment_type_str = t_type.treatment_type if t_type else "HD"
            treatment_code = treatment_type_str.upper()

            first_schedule = schedules[0] if schedules else None
            date_str = str(first_schedule.treatment_date) if first_schedule else ""
            formatted_date = first_schedule.treatment_date.strftime("%b %d, %Y") if first_schedule else ""

            shift_name = first_schedule.get_shift_display() if first_schedule else ""
            extra_count = len(schedules) - 1
            formatted_shift = f"{shift_name} (+{extra_count} More)" if extra_count > 0 else shift_name

            full_name = p_detail.full_name if p_detail else (appt.user.get_full_name() if appt.user else "Patient")
            initial = full_name[0].upper() if full_name else "P"

            data.append({
                "id": appt.id,
                "appointment_id": str(appt.appointment_id),
                "booking_id": booking_id,
                "patient": {
                    "full_name": full_name,
                    "email": p_detail.email if p_detail else (appt.user.email if appt.user else ""),
                    "phone": p_detail.phone if p_detail else "",
                    "avatar_initial": initial,
                },
                "treatment": {
                    "code": treatment_code,
                    "type": treatment_type_str
                },
                "dates_and_shift": {
                    "date": date_str,
                    "formatted_date": formatted_date,
                    "shift": first_schedule.shift if first_schedule else "",
                    "formatted_shift": formatted_shift,
                    "total_sessions": len(schedules)
                },
                "serology_and_health": {
                    "badge": serology_status,
                    "requires_isolation": is_isolation,
                    "hiv_positive": health.hivpositive if health else False,
                    "hvb_positive": health.hvbpositive if health else False,
                    "hcv_positive": health.hcvpositive if health else False,
                },
                "status": appt.status,
                "total_price": str(appt.total_price),
                "created_at": appt.created_at
            })
        return success(
            data={
                "counts": {
                    "total": total_count,
                    "pending": pending_count,
                    "confirmed": confirmed_count,
                    "completed": completed_count,
                    "cancelled": cancelled_count
                },
                "appointments": data
            },
            message="Clinic partner appointments retrieved successfully.",
            status_code=status.HTTP_200_OK
        )

    def patch(self, request, pk=None):
        appointment_id = pk or request.data.get('appointment_id') or request.data.get('id')
        new_status = request.data.get('status')
        if not appointment_id or not new_status:
            return error(message="appointment_id and status are required.", status_code=status.HTTP_400_BAD_REQUEST)

        valid_statuses = [choice[0] for choice in ClinicAppointment.STATUS_CHOICES]
        if new_status not in valid_statuses:
            return error(message=f"Invalid status. Allowed: {', '.join(valid_statuses)}", status_code=status.HTTP_400_BAD_REQUEST)

        try:
            appt = ClinicAppointment.objects.get(id=appointment_id)
        except ClinicAppointment.DoesNotExist:
            return error(message="Appointment not found.", status_code=status.HTTP_404_NOT_FOUND)

        appt.status = new_status
        appt.save()
        return success(
            data={"id": appt.id, "status": appt.status},
            message=f"Appointment status updated to '{new_status}' successfully.",
            status_code=status.HTTP_200_OK
        )

