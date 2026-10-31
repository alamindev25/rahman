from celery import shared_task
from django.core.mail import EmailMultiAlternatives
import logging

logger = logging.getLogger(__name__)

# Celery task to send emails template
@shared_task(bind=True, max_retries=3)
def send_email_task(self, subject, body, to_emails, from_email=None, html_body=None, attachments=None):
    try:
        email = EmailMultiAlternatives(
            subject=subject,
            body=body,
            from_email=from_email,
            to=to_emails,
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )

        if attachments:
            for attachment in attachments:
                email.attach(
                    attachment['filename'],
                    attachment['content'],
                    attachment['mimetype']
                )
        
        if html_body:
            email.attach_alternative(html_body, "text/html")
        
        # Send the email
        email.send()
        
        logger.info(f"Email sent successfully to {to_emails}")
        return {"status": "success", "message": f"Email sent to {to_emails}"}
        
    except Exception as exc:
        logger.error(f"Failed to send email to {to_emails}: {str(exc)}")
        # Retry the task after 60 seconds
        raise self.retry(exc=exc, countdown=60)
