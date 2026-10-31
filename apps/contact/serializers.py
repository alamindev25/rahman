from rest_framework import serializers
from .models import ContactInfo, ContactMessage

class ContactInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactInfo
        fields = ['id','address','email','phone','facebook','youtube','linkedin','twitter','instagram'  ]

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['id', 'full_name', 'email', 'query_type', 'message', 'created_at']