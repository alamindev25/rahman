import logging
import stripe
from decimal import Decimal
from django.conf import settings
from django.db import models
from django.utils import timezone
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.parsers import JSONParser, FormParser, MultiPartParser
from apps.user.authentication import JWTAuthentication
from apps.appoinment.models import ClinicAppointment
from .models import AppointmentPayment
from .serializers import (
    AppointmentPaymentSerializer,
    StripeCheckoutRequestSerializer,
)

logger = logging.getLogger(__name__)
stripe.api_key = getattr(settings, 'STRIPE_SECRET_KEY', '')


class AppointmentStripeCheckoutAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [JSONParser, FormParser, MultiPartParser]

    def post(self, request):
        serializer = StripeCheckoutRequestSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        appointment_param = serializer.validated_data['appointment_id']
        success_url = serializer.validated_data['success_url']
        cancel_url = serializer.validated_data['cancel_url']

        try:
            appointment = ClinicAppointment.objects.filter(
                user=request.user
            ).filter(
                models.Q(id=appointment_param) if str(appointment_param).isdigit() else models.Q(appointment_id=appointment_param)
            ).first()

            if not appointment:
                return Response(
                    {"error": "Appointment not found for the current user."},
                    status=status.HTTP_404_NOT_FOUND
                )
            # Determine price: appointment.total_price -> selected treatment price * schedules -> clinic per_treatment_price
            amount_val = Decimal(str(appointment.total_price or 0))
            if amount_val <= 0 and appointment.clinic:
                from apps.appoinment.serializers import get_clinic_treatment_price
                t_val = getattr(getattr(appointment, 'treatment_type', None), 'treatment_type', None)
                unit_p = get_clinic_treatment_price(appointment.clinic, t_val)
                if unit_p and unit_p > 0:
                    sched_cnt = Decimal(str(max(appointment.schedules.count(), 1)))
                    amount_val = Decimal(str(unit_p)) * sched_cnt
                else:
                    amount_val = Decimal(str(getattr(appointment.clinic, 'per_treatment_price', 0) or 0))

            if amount_val <= 0:
                amount_val = Decimal('150.00')

            # Update appointment.total_price if it was 0
            if appointment.total_price <= 0:
                appointment.total_price = amount_val
                appointment.save()

            unit_amount = int(amount_val * 100)

            clinic_name = "Clinic"
            if appointment.clinic:
                clinic_name = getattr(appointment.clinic, 'facility_name', None) or getattr(appointment.clinic, 'name', 'Clinic')

            # Create or get pending AppointmentPayment log record
            payment_record, _ = AppointmentPayment.objects.get_or_create(
                user=request.user,
                appointment=appointment,
                payment_status='pending',
                defaults={
                    'amount': amount_val,
                    'payment_gateway': 'stripe'
                }
            )
            payment_record.amount = amount_val
            payment_record.save()
            checkout_session = stripe.checkout.Session.create(
                payment_method_types=['card'],
                customer_email=request.user.email if (request.user and request.user.email) else None,
                line_items=[{
                    'price_data': {
                        'currency': 'usd',
                        'product_data': {
                            'name': f"Appointment at {clinic_name}",
                            'description': f"Appointment ID: {appointment.appointment_id}",
                        },
                        'unit_amount': unit_amount,
                    },
                    'quantity': 1,
                }],
                mode='payment',
                success_url=success_url,
                cancel_url=cancel_url,
                metadata={
                    'payment_record_id': str(payment_record.id),
                    'appointment_id': str(appointment.appointment_id),
                    'db_appointment_id': str(appointment.id),
                    'user_id': str(request.user.id),
                }
            )

            payment_record.checkout_session_id = checkout_session.id
            payment_record.save()

            return Response(
                {
                    "message": "Stripe checkout session created successfully",
                    "checkout_url": checkout_session.url,
                    "session_id": checkout_session.id,
                    "payment_id": payment_record.id,
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.exception("Failed to initiate Stripe checkout: %s", str(e))
            return Response(
                {"error": f"Failed to initiate Stripe checkout: {str(e)}"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class AppointmentPaymentHistoryAPIView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        payments = AppointmentPayment.objects.filter(user=request.user)
        serializer = AppointmentPaymentSerializer(payments, many=True)
        return Response(
            {
                "status": "success",
                "count": payments.count(),
                "data": serializer.data
            },
            status=status.HTTP_200_OK
        )


@method_decorator(csrf_exempt, name='dispatch')
class StripeWebhookAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    authentication_classes = []

    def post(self, request):
        payload = request.body
        sig_header = request.META.get('HTTP_STRIPE_SIGNATURE')
        endpoint_secret = getattr(settings, 'STRIPE_WEBHOOK_SECRET', '')

        try:
            if endpoint_secret and sig_header:
                event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
            elif settings.DEBUG:
                if isinstance(request.data, dict) and request.data:
                    event = request.data
                elif payload:
                    try:
                        import json
                        event = json.loads(payload.decode('utf-8'))
                    except Exception:
                        event = request.data if isinstance(request.data, dict) else {}
                else:
                    event = request.data if isinstance(request.data, dict) else {}
            else:
                event = stripe.Event.construct_from(request.data if isinstance(request.data, dict) else {}, stripe.api_key)
        except ValueError as e:
            logger.error("Invalid Stripe payload: %s", e)
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError as e:
            logger.error("Invalid Stripe signature: %s", e)
            return HttpResponse(status=400)
        except Exception as e:
            logger.error("Stripe Webhook error: %s", e)
            return HttpResponse(status=400)

        event_type = event.get('type')

        if event_type == 'checkout.session.completed':
            session = event['data']['object']
            session_id = session.get('id')
            metadata = session.get('metadata', {}) or {}
            payment_record_id = metadata.get('payment_record_id')
            appointment_id = metadata.get('appointment_id') or metadata.get('db_appointment_id')
            transaction_id = session.get('payment_intent') or session_id

            # Update AppointmentPayment record if found
            if payment_record_id:
                payment = AppointmentPayment.objects.filter(id=payment_record_id).first()
                if payment:
                    payment.payment_status = 'success'
                    payment.transaction_id = transaction_id
                    payment.save()

            # Update ClinicAppointment status
            if appointment_id:
                appointment = ClinicAppointment.objects.filter(
                    models.Q(id=appointment_id) if str(appointment_id).isdigit() else models.Q(appointment_id=appointment_id)
                ).first()

                if appointment:
                    appointment.payment_status = 'paid'
                    appointment.status = 'confirmed'
                    appointment.transaction_id = transaction_id
                    appointment.paid_at = timezone.now()
                    appointment.save()

        return HttpResponse(status=200)
