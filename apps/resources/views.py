from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.shortcuts import get_object_or_404

from .models import ResourceItem
from .serializers import ResourceItemSerializer,ResourceItemDetailsSerializer

class ResourceItemListView(APIView):
    permission_classes = [AllowAny]
    def get(self, request):
        resources = ResourceItem.objects.all().order_by("order")
        serializer = ResourceItemSerializer(
            resources, many=True, context={"request": request}
        )
        return Response(
            {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Resource items fetched successfully.",
                "data":serializer.data,
            },
            status=status.HTTP_200_OK,
        )                 
class ResourceItemDetailView(APIView):
    permission_classes = [AllowAny]
    def get(self, request, pk):
        resource = get_object_or_404(ResourceItem, pk=pk)
        serializer = ResourceItemDetailsSerializer(resource, context={"request": request})
        return Response(
            {
                "status": status.HTTP_200_OK,
                "success": True,
                "message": "Resource item retrieved successfully.",
                "data": serializer.data,
            },
            status=status.HTTP_200_OK,
        )