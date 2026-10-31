from django.db import models

class ContactInfo(models.Model):
    address = models.TextField(max_length=500, blank=True, null=True)
    email = models.EmailField( )
    phone = models.CharField(max_length=50)
    facebook = models.URLField(blank=True, null=True)
    youtube = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    def __str__(self):
        return "Contact & Social Information"

class ContactMessage(models.Model):
    QUERY_TYPES = [
    ('general_inquiry', 'General Inquiry'),
    ('book_appointment', 'Book an Appointment'),
    ('list_clinic', 'List My Clinic'),
    ('technical_support', 'Technical Support'),
    ('billing_payments', 'Billing & Payments'),
    ('partnership', 'Partnership'),
    ('other', 'Other'),
   ]
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    query_type = models.CharField(max_length=50, choices=QUERY_TYPES, default='general')
    message = models.TextField()
    is_agree = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.full_name} - {self.query_type}"
        