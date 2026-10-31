from rest_framework.response import Response
from rest_framework import status
from django.core.mail import EmailMultiAlternatives
from django.utils.html import format_html


def success(data=None, message="Success", status_code=status.HTTP_200_OK):
    return Response({
        "status": status_code,
        "success": True,
        "message": message,
        "data": data
    }, status=status_code)

def error(message="Error", errors=None, status_code=status.HTTP_400_BAD_REQUEST):
    return Response({
        "status": status_code,
        "success": False,
        "message": message,
        "errors": errors
    }, status=status_code)

def send_email(subject, body, to_emails, from_email=None, html_body=None, attachments=None):
    
    email = EmailMultiAlternatives(
        subject=subject,
        body=body,
        from_email=from_email,
        to=to_emails,
        headers={'X-Requested-With': 'XMLHttpRequest'}

    )

    if attachments:
        for attachment in attachments:
            email.attach(attachment['filename'], attachment['content'], attachment['mimetype'])
    
    if html_body:
        email.attach_alternative(html_body, "text/html")    
    # Send the email
    email.send()

def get_url(self, obj):
        if not getattr(obj, "thumbnail", None):
            return None

        try:
            url = obj.thumbnail.url
        except Exception:
            return None

        request = self.context.get("request")
        if request and url and url.startswith("/"):
            return request.build_absolute_uri(url)
        return url

def serialize_or_empty(model, serializer):
    
    if not model.objects.exists():
        return []
    queryset = model.objects.all()
    return serializer(queryset, many=True).data

def admin_image_preview(obj, field_name: str, height: int = 25, rounded: bool = True):
    image_field = getattr(obj, field_name, None)
    if not image_field:
        return "-"

    try:
        image_url = image_field.url
    except Exception:
        image_url = None

    if not image_url:
        return "-"

    style = f"height:{height}px;"
    if rounded:
        style += " border-radius:3px;"

    return format_html('<img src="{}" style="{}" />', image_url, style)


def admin_video_preview(obj, field_name):
    field = getattr(obj, field_name, None)
    if not field:
        return "— No Preview —"

    try:
        url = field.url
    except Exception:
        return "— Invalid File —"

    if url.lower().endswith(('.mp4', '.mov', '.webm', '.ogg')):
        return format_html(
            '<video width="320" height="180" controls style="border-radius:8px;">'
            '<source src="{}" type="video/mp4">'
            'Your browser does not support the video tag.'
            '</video>', url
        )
    else:
        return format_html(
            '<img src="{}" width="200" style="border-radius:8px; box-shadow:0 0 4px #aaa;" />', url
        )