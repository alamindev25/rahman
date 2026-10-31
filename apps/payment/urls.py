from django.urls import path
from .views import (
    AppointmentStripeCheckoutAPIView,
    AppointmentPaymentHistoryAPIView,
    StripeWebhookAPIView,
)
urlpatterns = [
    path('checkout/appointment/', AppointmentStripeCheckoutAPIView.as_view(), name='appointment-stripe-checkout'),
    path('history/', AppointmentPaymentHistoryAPIView.as_view(), name='appointment-payment-history'),
    path('webhook/stripe/', StripeWebhookAPIView.as_view(), name='stripe-payment-webhook'),
]
