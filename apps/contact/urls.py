from django.urls import path
from .views import HappyPatientStatView, ContactInfoView, ContactMessageCreateView

urlpatterns = [
    path('happy-patients/', HappyPatientStatView.as_view(), name='happy-patients'),
    path('contact-info/', ContactInfoView.as_view(), name='contact-info'),
    path('contact-submit/', ContactMessageCreateView.as_view(), name='contact-submit'),
]