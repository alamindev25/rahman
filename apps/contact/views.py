from django.shortcuts import render
# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import ContactInfo, ContactMessage
from .serializers import ContactInfoSerializer, ContactMessageSerializer
from rest_framework.permissions import AllowAny 

def get_patient_user_count():
    try:
        from apps.user.models import User
        count = User.objects.filter(role=User.Roles.PATIENT).count()
        if count == 0:
            count = User.objects.filter(role__in=['PATIENT', 'USER']).count()
        if count == 0:
            count = User.objects.exclude(role__in=['ADMIN', 'CLINIC_OWNER', 'admin', 'clinic_owner']).count()
        return f"{count}+"
    except Exception:
        return "0+"

class HappyPatientStatView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        patient_count_str = get_patient_user_count()
        return Response({
            "success": True,
            "badge_title": "Happy Patient",
            "happy_patients_count": patient_count_str,
            "data": {
                "badge_title": "Happy Patient",
                "happy_patients_count": patient_count_str
            }
        }, status=status.HTTP_200_OK)
        
class ContactInfoView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        contact_info = ContactInfo.objects.all()
        serializer = ContactInfoSerializer(contact_info, many=True, context={'request': request})
        return Response({
            "success": True,
            "data": serializer.data
        }, status=status.HTTP_200_OK)
        
class ContactMessageCreateView(APIView):
    permission_classes=[AllowAny]
    def post(self, request):
        serializer = ContactMessageSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "success": True,
                "message": "Message sent successfully!",
                "data":serializer.data
            }, status=status.HTTP_201_CREATED)
        return Response({
            "success": False,
            "errors":serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)