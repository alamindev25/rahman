from django.urls import path

from apps.appoinment.views import (
    ClinicAppointmentCreateAPIView,
    ClinicAppointmentDetailAPIView,
    BookedSlotsAPIView,
    UserBookingHistoryAPIView,
    # AppointmentReceiptDownloadAPIView
    ClinicSlotCapacityAPIView,
    AvailableSlotCheckingAPIView,
    ClinicAvailabilitySettingsAPIView,
    ClinicBlackoutDateAPIView,
)
urlpatterns = [
    path('appointments/', ClinicAppointmentCreateAPIView.as_view(), name='appointment-create'),
    path('appointments/<int:pk>/', ClinicAppointmentDetailAPIView.as_view(), name='appointment-detail'),
    # path('appointments/<int:pk>/receipt/', AppointmentReceiptDownloadAPIView.as_view(), name='appointment-receipt'),
    path('appointments/booked-slots/', BookedSlotsAPIView.as_view(), name='booked-slots'),
    path('booking-history/', UserBookingHistoryAPIView.as_view(), name='booking-history-api'),
    path('appointmentper-slot/', ClinicSlotCapacityAPIView.as_view(), name='appointment_book'),
    path('available-slots/', AvailableSlotCheckingAPIView.as_view(), name='available_slots_api'),
    path('slot-capacity/<int:pk>/', ClinicSlotCapacityAPIView.as_view(), name='clinic_slot_capacity_detail'),
    path('availability-shifts/', ClinicAvailabilitySettingsAPIView.as_view(), name='availability_shifts_settings'),
    path('blackout-dates/', ClinicBlackoutDateAPIView.as_view(), name='blackout_dates'),
    path('blackout-dates/<int:pk>/', ClinicBlackoutDateAPIView.as_view(), name='blackout_dates_detail'),
]