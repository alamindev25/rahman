from django.urls import path
from .views import (
    AdminClinicApproveView,
    AdminClinicRejectView,
    ClinicAdminDashboardListView,
    ClinicRegisterView,
    ClinicOwnerSignUpView,
    ClinicListAPIView,
    ClinicDetailAPIView,
    ClinicProfileCreateAPIView,
    CreateClinicRatingView,
    EmailApproveClinicView,
    EmailRejectClinicView,
    ClinicLocationDateSearchAPIView,
    HealthcareNetworkStatsAPIView,
    ClinicPartnerAppointmentsAPIView,
    ClinicSubmissionStatusAPIView,
    ClinicTreatmentListAPIView,
)

urlpatterns = [
    path('clinics/register/', ClinicRegisterView.as_view(), name='clinic-register'),
    path('clinics/submission-status/', ClinicSubmissionStatusAPIView.as_view(), name='clinic-submission-status'),
    # path('clinics/status/', ClinicSubmissionStatusAPIView.as_view(), name='clinic-status'),
    path('clinics/owner-register/', ClinicOwnerSignUpView.as_view(), name='clinic-owner-register'),
    path('auth/clinic-owner/signup/', ClinicOwnerSignUpView.as_view(), name='auth-clinic-owner-signup'),
    path('clinics/profile/', ClinicProfileCreateAPIView.as_view(), name='clinic-profile-create'),
    path('clinics/dashboard/', ClinicAdminDashboardListView.as_view(), name='clinic-admin-dashboard'),
    path('clinics/dashboard/appointments/', ClinicPartnerAppointmentsAPIView.as_view(), name='clinic-partner-appointments'),
    path('clinics/dashboard/appointments/<int:pk>/', ClinicPartnerAppointmentsAPIView.as_view(), name='clinic-partner-appointment-update'),
    path('clinics/', ClinicListAPIView.as_view(), name='clinic-list'),
    path('clinics/<int:pk>/', ClinicDetailAPIView.as_view(), name='clinic-detail'),
    path('clinics/treatments/', ClinicTreatmentListAPIView.as_view(), name='clinic-treatment-list'),
    path('treatments/', ClinicTreatmentListAPIView.as_view(), name='treatment-list'),
    path('clinics/rating/', CreateClinicRatingView.as_view(), name='clinic-rating'),
    path("clinic/<int:pk>/approve/", AdminClinicApproveView.as_view()),
    path("clinic/<int:pk>/reject/", AdminClinicRejectView.as_view()),
    path("clinic/email-approve/<uuid:token>/", EmailApproveClinicView.as_view()),
    path("clinic/email-reject/<uuid:token>/", EmailRejectClinicView.as_view()),
    path('clinic/search/', ClinicLocationDateSearchAPIView.as_view(), name='clinic_search_api'),
    path('clinic/stats/', HealthcareNetworkStatsAPIView.as_view(), name='healthcare_network_stats'),
]


