from django.conf import settings
from django.template.loader import render_to_string
from apps.utils.tasks import send_email_task
from apps.user.models import User


# Clinic Email Notifications
def send_clinic_pending_email(clinic):

    html_content = render_to_string(
        "clinic_pending.html",
        {
            "owner_email": clinic.owner.email,
            "clinic_name": clinic.clinic_name,
            "phone_number": clinic.phone_number,
            
        }
    )
    send_email_task.delay(
        subject="Clinic Registration Pending",
        body=(
            f"Your clinic {clinic.clinic_name} "
            "registration is pending."
        ),
        to_emails=[
            clinic.owner.email
        ],
        from_email=settings.EMAIL_HOST_USER,
        html_body=html_content
    )

# Clinic Email Notifications for Admin
def send_admin_clinic_request_email(clinic):
    super_admin_emails = User.objects.filter(
        is_superuser=True
    ).values_list(
        "email",
        flat=True
    )
    approve_url = (
    f"{settings.BACKEND_URL}/api/clinic/{clinic.id}/approve/")

    reject_url = (
    f"{settings.BACKEND_URL}/api/clinic/{clinic.id}/reject/")

    html_content = render_to_string(
        "clinic_approval_request.html",
        {
            "clinic_name": clinic.clinic_name,
            "owner_email": clinic.owner.email,
            "phone_number": clinic.phone_number,
            "approve_url": approve_url,
            "reject_url": reject_url,
        }
    )
    send_email_task.delay(
        subject="New Clinic Approval Request",
        body=(
            f"New clinic request: "
            f"{clinic.clinic_name}"
        ),
        to_emails=list(super_admin_emails),

        from_email=settings.EMAIL_HOST_USER,

        html_body=html_content
    )

# Clinic Email Notifications for Approval/Rejection
def send_clinic_approved_email(clinic):
    frontend_url = getattr(settings, 'FRONTEND_URL', 'http://127.0.0.1:8000')
    if "127.0.0.1:8000" in frontend_url or "localhost:8000" in frontend_url:
        login_url = f"{frontend_url}/api/signin/"
    else:
        login_url = f"{frontend_url}/login"

    html_content = render_to_string(
        "clinic_approved.html",
        {
            "owner_email": clinic.owner.email,
            "clinic_name": clinic.clinic_name,
            "login_url": login_url,
        }
    )
    send_email_task.delay(
        subject="Clinic Registration Approved",
        body=(
            f"Your clinic {clinic.clinic_name} "
            f"has been approved. You can log in at: {login_url}"
        ),
        to_emails=[
            clinic.owner.email
        ],
        from_email=settings.EMAIL_HOST_USER,
        html_body=html_content
    )

# Clinic Email Notifications for Rejection
def send_clinic_rejected_email(clinic, reason=None):
    html_content = render_to_string(
        "clinic_rejected.html",
        {
            "owner_email": clinic.owner.email,
            "clinic_name": clinic.clinic_name,
            "reason": reason or "No reason provided."
        }
    )
    send_email_task.delay(
        subject="Clinic Registration Rejected",
        body=(
            f"Your clinic {clinic.clinic_name} "
            "registration has been rejected."
        ),
        to_emails=[
            clinic.owner.email
        ],
        from_email=settings.EMAIL_HOST_USER,
        html_body=html_content
    )