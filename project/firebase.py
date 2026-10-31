import firebase_admin
from firebase_admin import credentials
from firebase_admin import messaging


# Initialize Firebase Admin
def initialize_firebase():
    if not firebase_admin._apps:
        cred = credentials.Certificate(
            "serviceAccountKey.json"
        )
        firebase_admin.initialize_app(cred)

# Function to send push notifications (No need when i call from notification utils)
def send_push_notification(user, title, body, data=None):
    from apps.notification.models import DeviceToken
    tokens = DeviceToken.objects.filter(
        user=user
    ).values_list('token', flat=True)

    if not tokens:
        return

    message = messaging.MulticastMessage(
        notification=messaging.Notification(
            title=title,
            body=body
        ),
        data=data or {},
        tokens=list(tokens)
    )

    response = messaging.send_each_for_multicast(message)

    return response

