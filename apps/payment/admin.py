from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AppointmentPayment


@admin.register(AppointmentPayment)
class AppointmentPaymentAdmin(ModelAdmin):
    list_display = (
        'id',
        'user',
        'appointment',
        'amount',
        'payment_gateway',
        'payment_status',
        'transaction_id',
        'created_at'
    )
    list_filter = ('payment_gateway', 'payment_status', 'created_at')
    search_fields = ('user__email', 'appointment__appointment_id', 'transaction_id', 'checkout_session_id')

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Auto-sync pending payments directly with Stripe API when Admin page is opened/refreshed
        pending_payments = list(qs.filter(payment_status='pending', checkout_session_id__isnull=False))
        if pending_payments:
            from .views import sync_pending_payment
            for payment in pending_payments:
                sync_pending_payment(payment)
            qs = super().get_queryset(request)
        return qs
