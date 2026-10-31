from django.db import models
from django.conf import settings
from apps.appoinment.models import ClinicAppointment


class AppointmentPayment(models.Model):
    PAYMENT_GATEWAY_CHOICES = (
        ('stripe', 'Stripe'),
        ('cash', 'Cash / Pay at Clinic'),
    )
    PAYMENT_STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('success', 'Success'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='appointment_payments'
    )
    appointment = models.ForeignKey(
        ClinicAppointment,
        on_delete=models.CASCADE,
        related_name='payment_records'
    )
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_gateway = models.CharField(
        max_length=50,
        choices=PAYMENT_GATEWAY_CHOICES,
        default='stripe'
    )
    payment_status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS_CHOICES,
        default='pending'
    )
    transaction_id = models.CharField(max_length=255, null=True, blank=True)
    checkout_session_id = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Payment {self.id} - Appointment {self.appointment_id} ({self.payment_status})"
    
