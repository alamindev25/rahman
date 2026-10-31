from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .config import PAGE_MAP
from apps.utils.helpers import serialize_or_empty
from rest_framework.permissions import AllowAny
from .serializers import AboutContactSubmissionSerializer, DemoBookingSerializer,FAQSerializer
from .models import FAQ

class CMSPageView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        page_name = request.query_params.get("page_name")
        section_name = request.query_params.get("section_name")

        # Specific Page Request (Ex: landing, about_us, pricing, resource, blog)
        if page_name:
            if page_name not in PAGE_MAP:
                return Response({
                    "status": status.HTTP_404_NOT_FOUND,
                    "success": False,
                    "message": f"Page '{page_name}' not found.",
                    "data": {}
                }, status=status.HTTP_404_NOT_FOUND)

            # Specific Section (Ex: nav, hero, integration, features, clinicore, compliance, howitworks, ....)
            if section_name:
                section_map = PAGE_MAP[page_name].get(section_name)
                if not section_map:
                    return Response({
                        "status": status.HTTP_404_NOT_FOUND,
                        "success": False,
                        "message": f"Section '{section_name}' not found in '{page_name}' page.",
                        "data": {}
                    }, status=status.HTTP_404_NOT_FOUND)

                model, serializer = section_map
                # check if section has data
                if not model.objects.exists():
                    return Response({
                        "status": status.HTTP_204_NO_CONTENT,
                        "success": True,
                        "message": f"No data found for '{section_name}' section in '{page_name}' page.",
                        "data": []
                    }, status=status.HTTP_204_NO_CONTENT)
                data = serialize_or_empty(model, serializer)
                return Response({
                    "status": status.HTTP_200_OK,
                    "success": True,
                    "message": f"'{page_name}' page → '{section_name}' section fetched successfully.",
                    "data": {section_name: data}
                }, status=status.HTTP_200_OK)
            # Full Page Data
            page_data = {}
            for section_name, (model, serializer) in PAGE_MAP[page_name].items():
                page_data[section_name] = serialize_or_empty(model, serializer)

            return Response({
                "status": status.HTTP_200_OK,
                "success": True,
                "message": f"'{page_name}' page fetched successfully.",
                "data": {page_name: page_data}
            }, status=status.HTTP_200_OK)

        # Full CMS (No page_name)
        cms_data = {}
        for page, sections in PAGE_MAP.items():
            cms_data[page] = {}
            for section_name, (model, serializer) in sections.items():
                cms_data[page][section_name] = serialize_or_empty(model, serializer)

        return Response({
            "status": status.HTTP_200_OK,
            "success": True,
            "message": "Full CMS fetched successfully.",
            "data": cms_data,
        }, status=status.HTTP_200_OK)
    def post(self, request):
            page_name = request.query_params.get("page_name")
            section_name = request.query_params.get("section_name")

            # Contact Submission
            if page_name == "about_us" and section_name == "contact_submission":
                serializer = AboutContactSubmissionSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": status.HTTP_201_CREATED,
                        "success": True,
                        "message": "Thank you for contacting us! We'll get back to you soon."
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Demo Booking
            elif page_name == "demo" and section_name == "demo_booking":
                serializer = DemoBookingSerializer(data=request.data)
                if serializer.is_valid():
                    serializer.save()
                    return Response({
                        "status": status.HTTP_201_CREATED,
                        "success": True,
                        "message": "Demo Booking Saved.",
                        "data": serializer.data
                    }, status=status.HTTP_201_CREATED)
                return Response({
                    "status": status.HTTP_400_BAD_REQUEST,
                    "success": False,
                    "errors": serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

            # Invalid combination
            return Response({
                "status": status.HTTP_405_METHOD_NOT_ALLOWED,
                "success": False,
                "message": "POST method is only allowed for valid sections (About Us Contact or Demo Booking)."
            },status=status.HTTP_405_METHOD_NOT_ALLOWED)

class FAQListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, format=None):
        faqs = FAQ.objects.filter(status=True)
        serializer = FAQSerializer(faqs, many=True)
        return Response({
            "status": "success",
            "count": faqs.count(),
            "data": serializer.data
        }, status=status.HTTP_200_OK)