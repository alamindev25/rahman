from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions

from apps.utils.helpers import error, success

from apps.appoinment.models import (
    ClinicAppointment,
    TreatmentSchedule,
    ClinicSlotCapacity,
    ClinicWeeklySchedule,
    ClinicShiftTiming,
    ClinicBlackoutDate,
)
from apps.clinic.models import ClinicRegister, ClinicProfile
from .serializers import (
    ClinicAppointmentSerializer,
    ClinicSlotCheckingSerializer,
    ClinicSlotCapacitySerializer,
    BookingHistorySerializer,
    AppointmentStatusUpdateSerializer,
    ClinicWeeklyScheduleSerializer,
    ClinicShiftTimingSerializer,
    ClinicBlackoutDateSerializer,
)
import json
from rest_framework.parsers import MultiPartParser, FormParser
# ClinicAppointment
class ClinicAppointmentCreateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [ MultiPartParser,FormParser]
    def get(self, request):
        user = request.user
        if user.is_superuser or user.is_staff:
            appointments = ClinicAppointment.objects.all()
        elif getattr(user, 'role', None) == 'CLINIC_OWNER' or ClinicRegister.objects.filter(Q(owner=user) | Q(clinic_admin=user)).exists():
            appointments = ClinicAppointment.objects.filter(
                Q(clinic__clinic__owner=user) | Q(clinic__clinic__clinic_admin=user) | Q(user=user)
            ).distinct()
        else:
            appointments = ClinicAppointment.objects.filter(user=user)

        base_appointments = appointments

        clinic_id = request.query_params.get('clinic_id') or request.query_params.get('clinic')
        if clinic_id:
            base_appointments = base_appointments.filter(clinic_id=clinic_id)

        # Status summary breakdown for UI tab/badge counts (Total, Pending, Confirmed, Completed, Cancelled)
        summary = {
            "total": base_appointments.count(),
            "pending": base_appointments.filter(status='pending').count(),
            "confirmed": base_appointments.filter(status='confirmed').count(),
            "completed": base_appointments.filter(status='completed').count(),
            "cancelled": base_appointments.filter(status='cancelled').count(),
        }
        appointments = base_appointments

        # Filter by status parameter (e.g. status=pending, status=confirmed, status=confirm, status=completed, status=cancelled)
        status_param = request.query_params.get('status')
        if status_param and str(status_param).lower() != 'all':
            st_clean = str(status_param).lower().strip()
            if st_clean in ['confirm', 'confirmed']:
                appointments = appointments.filter(status='confirmed')
            elif st_clean in ['pending', 'completed', 'cancelled']:
                appointments = appointments.filter(status=st_clean)
            else:
                appointments = appointments.filter(status__iexact=st_clean)

        # Search parameter (by patient name, email, phone, booking ID)
        search_query = request.query_params.get('search') or request.query_params.get('q')
        if search_query:
            search_query = str(search_query).strip()
            appointments = appointments.filter(
                Q(patient_detail__full_name__icontains=search_query) |
                Q(patient_detail__email__icontains=search_query) |
                Q(patient_detail__phone__icontains=search_query) |
                Q(appointment_id__icontains=search_query) |
                Q(id__icontains=search_query)
            ).distinct()

        appointments = appointments.select_related(
            'user',
            'clinic',
            'patient_detail',
            'health_status',
            'insurance',
            'treatment_type',
            'care_partner',
            'home_clinic'
        ).prefetch_related(
            'schedules',
            'medical_reports'
        ).order_by("-created_at")

        serializer = ClinicAppointmentSerializer(appointments, many=True, context={'request': request})
        return success(
            {
                "message": "Appointment list retrieved successfully",
                "summary": summary,
                "total_appointments": summary["total"],
                "count": appointments.count(),
                "data": serializer.data,
            },
        )
    
    def post(self, request):
        data = request.data.copy()
        json_fields = [
            'patient_detail',
            'schedules',
            'health_status',
            'insurance',
            'treatment_type',
            'care_partner',
            'home_clinic',
        ]
        for field in json_fields:
            if field in data:
                try:
                    data[field] = json.loads(data[field])
                except json.JSONDecodeError:
                    return Response(
                        {
                            "error": f"Invalid JSON format in {field}"
                        },
                        status=status.HTTP_400_BAD_REQUEST
                    )

        serializer = ClinicAppointmentSerializer(
            data=data,
            context={'request': request}
        )
        if serializer.is_valid():
            appointment = serializer.save()
            return Response(
                {
                    "message": "Appointment created successfully",
                    "data": ClinicAppointmentSerializer(
                        appointment,
                        context={'request': request}
                    ).data
                },
                status=status.HTTP_201_CREATED
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

# ClinicAppointment Detail, Update & Delete
class ClinicAppointmentDetailAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return ClinicAppointment.objects.select_related(
                'user', 'clinic', 'patient_detail', 'health_status', 'insurance', 'treatment_type', 'care_partner', 'home_clinic'
            ).prefetch_related('schedules', 'medical_reports').get(id=pk)
        except ClinicAppointment.DoesNotExist:
            return None

    def has_permission(self, request, appointment):
        user = request.user
        if user.is_superuser or user.is_staff:
            return True
        if appointment.user == user:
            return True
        if appointment.clinic and hasattr(appointment.clinic, 'clinic'):
            clinic_reg = appointment.clinic.clinic
            if clinic_reg and (clinic_reg.owner == user or clinic_reg.clinic_admin == user):
                return True
        return False

    def get(self, request, pk):
        appointment = self.get_object(pk)
        if not appointment:
            return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        if not self.has_permission(request, appointment):
            return Response({"message": "You do not have permission to view this appointment"}, status=status.HTTP_403_FORBIDDEN)
        serializer = ClinicAppointmentSerializer(appointment, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, pk):
        appointment = self.get_object(pk)
        if not appointment:
            return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        if not self.has_permission(request, appointment):
            return Response({"message": "You do not have permission to update this appointment"}, status=status.HTTP_403_FORBIDDEN)
        if 'status' in request.data:
            serializer = AppointmentStatusUpdateSerializer(appointment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                updated = self.get_object(pk)
                return Response(
                    {
                        "message": f"Appointment status updated to '{updated.status}' successfully",
                        "data": ClinicAppointmentSerializer(updated, context={'request': request}).data
                    },
                    status=status.HTTP_200_OK
                )
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer = ClinicAppointmentSerializer(appointment, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            updated = self.get_object(pk)
            return Response(ClinicAppointmentSerializer(updated, context={'request': request}).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        return self.patch(request, pk)
    def delete(self, request, pk):
        appointment = self.get_object(pk)
        if not appointment:
            return Response({"message": "Appointment not found"}, status=status.HTTP_404_NOT_FOUND)
        if not self.has_permission(request, appointment):
            return Response({"message": "You do not have permission to delete this appointment"}, status=status.HTTP_403_FORBIDDEN)
        appointment.delete()
        return Response({"message": "Appointment deleted successfully!"}, status=status.HTTP_200_OK)

class BookedSlotsAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        clinic_id = request.query_params.get('clinic_id') or request.query_params.get('clinic')
        if not clinic_id: 
            return Response(
                {"error": "clinic_id query parameter is required"},
                status=status.HTTP_400_BAD_REQUEST
            )
        queryset = TreatmentSchedule.objects.filter(
            appointment__clinic_id=clinic_id
        ).exclude(
            appointment__status='cancelled'
        )
        # Date range filtering (Best practice for performance)
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')
        year = request.query_params.get('year')
        month = request.query_params.get('month')
        if start_date and end_date:
            queryset = queryset.filter(treatment_date__range=[start_date, end_date])
        elif year and month:
            queryset = queryset.filter(treatment_date__year=year, treatment_date__month=month)
        booked_schedules = queryset.values('treatment_date', 'shift').distinct()
        return Response(
            {
                "clinic_id": clinic_id,
                "count": booked_schedules.count(),
                "booked_slots": list(booked_schedules)
            },
            status=status.HTTP_200_OK
        )

class UserBookingHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request):
        user = request.user
        if user.is_superuser or user.is_staff:
            appointments = ClinicAppointment.objects.all()
        elif getattr(user, 'role', None) == 'CLINIC_OWNER' or ClinicRegister.objects.filter(Q(owner=user) | Q(clinic_admin=user)).exists():
            appointments = ClinicAppointment.objects.filter(
                Q(clinic__clinic__owner=user) | Q(clinic__clinic__clinic_admin=user) | Q(user=user)
            ).distinct()
        else:
            appointments = ClinicAppointment.objects.filter(user=user)

        appointments = appointments.select_related(
            'clinic', 
            'treatment_type'
        ).prefetch_related(
            'schedules', 
            'medical_reports'
        ).order_by('-created_at')
        total_appointments = appointments.count()
        serializer = BookingHistorySerializer(appointments, many=True, context={'request': request})
        return success(
            data={
                "total_appointments": total_appointments,
                "count": total_appointments,
                "appointments": serializer.data
            },
            message="Booking history retrieved successfully."
        )

class ClinicSlotCapacityAPIView(APIView):
    def get(self, request):
        clinic_id = request.GET.get('clinic_id')
        if clinic_id:
            slots = ClinicSlotCapacity.objects.filter(clinic_id=clinic_id)
        else:
            slots = ClinicSlotCapacity.objects.all()
        serializer = ClinicSlotCapacitySerializer(slots, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # def post(self, request):
    #     serializer = ClinicSlotCapacitySerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save()
    #         return Response(
    #             {
    #                 "message": "Slot capacity saved successfully!",
    #                 "data": serializer.data
    #             }, 
    #             status=status.HTTP_201_CREATED
    #         )
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        clinic_id = request.data.get("clinic")
        date = request.data.get("date")
        shift = request.data.get("shift")
        max_limit = request.data.get("max_limit")

        if not clinic_id or not date or not shift or max_limit is None:
            return Response(
                {"error": "clinic, date, shift and max_limit are required."},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        slot, created = ClinicSlotCapacity.objects.update_or_create(
            clinic_id=clinic_id,
            date=date,
            shift=shift,
            defaults={
                "max_limit": max_limit
            }
        )
        serializer = ClinicSlotCapacitySerializer(slot)
        return Response(
            {
                "message": (
                    "Slot capacity created successfully!"
                    if created
                    else "Slot capacity updated successfully!"
                ),
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )
    def put(self, request, pk=None):
        slot_id = pk or request.data.get('id')
        if not slot_id:
            return Response({"error": "Slot ID is required for update."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            slot = ClinicSlotCapacity.objects.get(pk=slot_id)
        except ClinicSlotCapacity.DoesNotExist:
            return Response({"error": "Slot capacity not found."}, status=status.HTTP_404_NOT_FOUND)
        serializer = ClinicSlotCapacitySerializer(slot, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    "message": "Slot capacity updated successfully!",
                    "data": serializer.data
                }, 
                status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk=None):
        slot_id = pk or request.GET.get('id') or request.data.get('id')
        if not slot_id:
            return Response({"error": "Slot ID is required for deletion."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            slot = ClinicSlotCapacity.objects.get(pk=slot_id)
        except ClinicSlotCapacity.DoesNotExist:
            return Response({"error": "Slot capacity not found."}, status=status.HTTP_404_NOT_FOUND)
        slot.delete()
        return Response(
            {"message": "Slot capacity deleted successfully!"}, 
            status=status.HTTP_200_OK
        )


class AvailableSlotCheckingAPIView(APIView):
    def get(self, request):
        clinic_id = request.GET.get('clinic_id')
        date_query = request.GET.get('date') 
        if not clinic_id:
            return Response({"error": "Please provide a clinic_id parameter."}, status=status.HTTP_400_BAD_REQUEST)
        slot_capacities = ClinicSlotCapacity.objects.filter(clinic_id=clinic_id)
        if date_query:
            slot_capacities = slot_capacities.filter(date=date_query)
        available_slots_list = []
        for slot in slot_capacities:
            booked_count = TreatmentSchedule.objects.filter(
                appointment__clinic_id=clinic_id,
                treatment_date=slot.date,
                shift=slot.shift,
                appointment__status__in=['pending', 'confirmed']
            ).count()
            max_limit = slot.max_limit
            available_slots = max_limit - booked_count
            available_slots_list.append({
                "date": slot.date,
                "shift": slot.shift,
                "max_limit": max_limit,
                "booked_count": booked_count,
                "available_slots": max_limit if available_slots < 0 else available_slots,
                "is_full": booked_count >= max_limit
            })
        return Response({
            "clinic_id": clinic_id,
            "available_slots": available_slots_list
        },status=status.HTTP_200_OK)


class ClinicAvailabilitySettingsAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_clinic(self, request):
        clinic_id = request.query_params.get('clinic_id') or request.query_params.get('clinic')
        if clinic_id:
            try:
                return ClinicProfile.objects.get(id=clinic_id)
            except ClinicProfile.DoesNotExist:
                return None
        user = request.user
        profile = ClinicProfile.objects.filter(
            Q(clinic__owner=user) | Q(clinic__clinic_admin=user)
        ).first()
        if profile:
            return profile
        return ClinicProfile.objects.first()

    def get(self, request):
        clinic = self.get_clinic(request)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        # 1. Ensure Weekly Schedule entries for Mon-Sun exist
        days = ['mon', 'tue', 'wed', 'thu', 'fri', 'sat', 'sun']
        for d in days:
            default_open = (d != 'sun')
            ClinicWeeklySchedule.objects.get_or_create(
                clinic=clinic,
                day_of_week=d,
                defaults={'is_open': default_open}
            )
        weekly_schedules = ClinicWeeklySchedule.objects.filter(clinic=clinic).order_by('id')

        # 2. Ensure Shift Timings entries for morning, afternoon, evening exist
        default_shifts = [
            ('morning', '08:00:00', '12:00:00'),
            ('afternoon', '13:00:00', '17:00:00'),
            ('evening', '18:00:00', '22:00:00'),
        ]
        for s_code, start_t, end_t in default_shifts:
            ClinicShiftTiming.objects.get_or_create(
                clinic=clinic,
                shift=s_code,
                defaults={
                    'is_enabled': True,
                    'start_time': start_t,
                    'end_time': end_t,
                    'capacity': 6
                }
            )
        shift_timings = ClinicShiftTiming.objects.filter(clinic=clinic).order_by('id')

        # 3. Blackout & Maintenance Dates
        blackout_dates = ClinicBlackoutDate.objects.filter(clinic=clinic).order_by('date')

        return success({
            "clinic_id": clinic.id,
            "clinic_name": clinic.name or getattr(clinic.clinic, 'clinic_name', ''),
            "weekly_schedule": ClinicWeeklyScheduleSerializer(weekly_schedules, many=True).data,
            "shift_timings": ClinicShiftTimingSerializer(shift_timings, many=True).data,
            "blackout_dates": ClinicBlackoutDateSerializer(blackout_dates, many=True).data,
        })

    def post(self, request):
        clinic = self.get_clinic(request)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # Update Weekly Schedule
        weekly_data = data.get('weekly_schedule', [])
        for item in weekly_data:
            d_code = item.get('day_of_week')
            is_open = item.get('is_open', True)
            if d_code:
                ClinicWeeklySchedule.objects.update_or_create(
                    clinic=clinic,
                    day_of_week=d_code,
                    defaults={'is_open': is_open}
                )

        # Update Shift Timings & Bed Capacities
        shift_data = data.get('shift_timings', [])
        for item in shift_data:
            s_code = item.get('shift')
            if s_code:
                defaults = {}
                if 'is_enabled' in item:
                    defaults['is_enabled'] = item['is_enabled']
                if 'start_time' in item:
                    defaults['start_time'] = item['start_time']
                if 'end_time' in item:
                    defaults['end_time'] = item['end_time']
                if 'capacity' in item:
                    defaults['capacity'] = item['capacity']

                ClinicShiftTiming.objects.update_or_create(
                    clinic=clinic,
                    shift=s_code,
                    defaults=defaults
                )

        # Sync/Add Blackout & Maintenance Dates if provided
        blackout_data = data.get('blackout_dates', None)
        if isinstance(blackout_data, list):
            for item in blackout_data:
                b_date = item.get('date')
                b_reason = item.get('reason', '')
                if b_date:
                    ClinicBlackoutDate.objects.update_or_create(
                        clinic=clinic,
                        date=b_date,
                        defaults={'reason': b_reason}
                    )
        return self.get(request)
    def put(self, request):
        return self.post(request)


#new add
    def patch(self, request):
        clinic = self.get_clinic(request)

        if not clinic:
            return Response(
                {"error": "Clinic not found"},
                status=status.HTTP_404_NOT_FOUND
            )

        data = request.data

        # 1. Update Weekly Schedule
        weekly_data = data.get('weekly_schedule', [])

        for item in weekly_data:
            d_code = item.get('day_of_week')

            if not d_code:
                continue

            defaults = {}

            if 'is_open' in item:
                defaults['is_open'] = item['is_open']

            if defaults:
                ClinicWeeklySchedule.objects.update_or_create(
                    clinic=clinic,
                    day_of_week=d_code,
                    defaults=defaults
                )

        # 2. Update Shift Timings & Capacity
        shift_data = data.get('shift_timings', [])

        for item in shift_data:
            s_code = item.get('shift')

            if not s_code:
                continue

            allowed_fields = [
                'is_enabled',
                'start_time',
                'end_time',
                'capacity',
            ]

            defaults = {
                field: item[field]
                for field in allowed_fields
                if field in item
            }

            if defaults:
                ClinicShiftTiming.objects.update_or_create(
                    clinic=clinic,
                    shift=s_code,
                    defaults=defaults
                )

        # 3. Update Blackout & Maintenance Dates
        blackout_data = data.get('blackout_dates')

        if isinstance(blackout_data, list):
            for item in blackout_data:
                b_date = item.get('date')

                if not b_date:
                    continue

                defaults = {}

                if 'reason' in item:
                    defaults['reason'] = item['reason']

                if defaults:
                    ClinicBlackoutDate.objects.update_or_create(
                        clinic=clinic,
                        date=b_date,
                        defaults=defaults
                    )

        return self.get(request)


class ClinicBlackoutDateAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get_clinic(self, request):
        clinic_id = request.query_params.get('clinic_id') or request.query_params.get('clinic')
        if clinic_id:
            try:
                return ClinicProfile.objects.get(id=clinic_id)
            except ClinicProfile.DoesNotExist:
                return None
        user = request.user
        profile = ClinicProfile.objects.filter(
            Q(clinic__owner=user) | Q(clinic__clinic_admin=user)
        ).first()
        return profile or ClinicProfile.objects.first()

    def get(self, request):
        clinic = self.get_clinic(request)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)
        dates = ClinicBlackoutDate.objects.filter(clinic=clinic).order_by('date')
        serializer = ClinicBlackoutDateSerializer(dates, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        clinic = self.get_clinic(request)
        if not clinic:
            return Response({"error": "Clinic not found"}, status=status.HTTP_404_NOT_FOUND)
        date_val = request.data.get('date')
        reason_val = request.data.get('reason', '')
        if not date_val:
            return Response({"error": "Date is required"}, status=status.HTTP_400_BAD_REQUEST)
        obj, created = ClinicBlackoutDate.objects.update_or_create(
            clinic=clinic,
            date=date_val,
            defaults={'reason': reason_val}
        )
        serializer = ClinicBlackoutDateSerializer(obj)
        return Response(
            {
                "message": "Blackout date added successfully!" if created else "Blackout date updated successfully!",
                "data": serializer.data
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK
        )

    def delete(self, request, pk=None):
        blackout_id = pk or request.query_params.get('id') or request.data.get('id')
        if not blackout_id:
            return Response({"error": "ID is required for deletion"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            obj = ClinicBlackoutDate.objects.get(pk=blackout_id)
            obj.delete()
            return Response({"message": "Blackout date deleted successfully!"}, status=status.HTTP_200_OK)
        except ClinicBlackoutDate.DoesNotExist:
            return Response({"error": "Blackout date not found"}, status=status.HTTP_404_NOT_FOUND)




# from django.http import HttpResponse
# from io import BytesIO
# class AppointmentReceiptDownloadAPIView(APIView):
#     permission_classes = [permissions.IsAuthenticated]
#     def get(self, request, pk):
#         try:
#             appointment = ClinicAppointment.objects.select_related(
#                 'clinic', 'treatment_type', 'patient_detail'
#             ).prefetch_related('schedules').get(pk=pk)
#         except ClinicAppointment.DoesNotExist:
#             return Response({"error": "Appointment not found."}, status=status.HTTP_404_NOT_FOUND)
#         if appointment.user != request.user and not request.user.is_staff:
#             if not (appointment.clinic and hasattr(appointment.clinic, 'clinic') and (appointment.clinic.clinic.owner == request.user or appointment.clinic.clinic.clinic_admin == request.user)):
#                 return Response({"error": "You do not have permission to view this receipt."}, status=status.HTTP_403_FORBIDDEN)
#         serializer = BookingHistorySerializer(appointment, context={'request': request})
#         data = serializer.data
#         try:
#             from reportlab.lib.pagesizes import letter
#             from reportlab.pdfgen import canvas
#             from reportlab.lib import colors
#             buffer = BytesIO()
#             p = canvas.Canvas(buffer, pagesize=letter)
#             width, height = letter
#             # Title
#             p.setFont("Helvetica-Bold", 18)
#             p.drawString(50, height - 50, "BOOKING RECEIPT")
            
#             p.setFont("Helvetica-Bold", 14)
#             clinic_title = str(data.get('clinic_name') or 'Clinic')
#             p.drawString(50, height - 80, clinic_title)
#             p.setFont("Helvetica", 10)
#             p.setFillColor(colors.HexColor("#666666"))
#             booking_id_str = f"Booking ID: BK-{str(data.get('appointment_id'))[:8].upper()}"
#             p.drawString(50, height - 100, booking_id_str)
#             p.drawString(50, y, "Treatment Type")
#             p.drawString(180, y, "Treatment Dates")
#             p.drawString(330, y, "Selected Shift")
#             p.drawString(450, y, "Location")
#             y -= 20
#             p.setFont("Helvetica", 9)
#             p.setFillColor(colors.HexColor("#555555"))
#             p.drawString(50, y, str(data.get('treatment_type') or 'N/A'))
#             p.drawString(180, y, str(data.get('treatment_dates') or 'N/A'))
#             p.drawString(330, y, str(data.get('selected_shift') or 'N/A'))
#             loc = data.get('location') or {}
#             loc_str = ""
#             if isinstance(loc, dict):
#                 loc_str = ", ".join([x for x in [loc.get('city'), loc.get('country')] if x])
#             else:
#                 loc_str = str(loc)
#             p.drawString(450, y, loc_str or 'N/A')
#             # Patient Detail section if present
#             if hasattr(appointment, 'patient_detail') and appointment.patient_detail:
#                 pd = appointment.patient_detail
#                 y -= 40
#                 p.line(50, y + 20, width - 50, y + 20)
#                 p.setFont("Helvetica-Bold", 12)
#                 p.setFillColor(colors.black)
#                 p.drawString(50, y, "Patient Information")
                
#                 y -= 20
#                 p.setFont("Helvetica", 10)
#                 p.setFillColor(colors.HexColor("#444444"))
#                 p.drawString(50, y, f"Name: {pd.full_name}")
#                 p.drawString(250, y, f"Email: {pd.email}")
#                 y -= 18
#                 p.drawString(50, y, f"Phone: {pd.phone}")
#                 p.drawString(250, y, f"Language: {pd.language}")
#             p.setFont("Helvetica-Oblique", 8)
#             p.setFillColor(colors.HexColor("#888888"))
#             p.drawString(50, 40, "Thank you for booking with us. Generated automatically.")
#             p.showPage()
#             p.save()
#             buffer.seek(0)
#             response = HttpResponse(buffer.getvalue(), content_type='application/pdf')
#             response['Content-Disposition'] = f'attachment; filename="receipt_{appointment.id}.pdf"'
#             return response
#         except ImportError:
#             return Response({
#                 "message": "Receipt details",
#                 "receipt": data
#             }, status=status.HTTP_200_OK)