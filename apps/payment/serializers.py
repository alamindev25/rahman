from rest_framework import serializers
from .models import AppointmentPayment


class AppointmentPaymentSerializer(serializers.ModelSerializer):
    appointment_uuid = serializers.CharField(source='appointment.appointment_id', read_only=True)

    class Meta:
        model = AppointmentPayment
        fields = [
            'id',
            'user',
            'appointment',
            'appointment_uuid',
            'amount',
            'payment_gateway',
            'payment_status',
            'transaction_id',
            'checkout_session_id',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'user', 'created_at', 'updated_at']

class StripeCheckoutRequestSerializer(serializers.Serializer):
    appointment_id = serializers.CharField(required=True, help_text="Clinic Appointment ID (DB ID or UUID)")
    success_url = serializers.URLField(required=True, help_text="Redirect URL on payment success")
    cancel_url = serializers.URLField(required=True, help_text="Redirect URL on payment cancel")
