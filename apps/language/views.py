from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.db.utils import OperationalError
from django.core.management import call_command
from .models import Language
from .serializers import LanguageSerializer
from .seed_data import seed_languages


def ensure_language_table():
    try:
        Language.objects.first()
    except OperationalError:
        print("Table 'language_language' not found. Migrating automatically...")
        try:
            call_command('migrate')
            seed_languages()
        except Exception as e:
            print("Failed to auto-migrate language app:", e)
    else:
        try:
            call_command('migrate')
        except Exception:
            pass


class LanguageListAPIView(APIView):
    """
    Get all active languages for frontend language selector.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ensure_language_table()
        languages = Language.objects.filter(is_active=True).order_by('-is_default', 'name')
        serializer = LanguageSerializer(languages, many=True, context={'request': request})
        return Response(
            {
                "message": "Languages retrieved successfully",
                "count": languages.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )


class DefaultLanguageAPIView(APIView):
    """
    Get the default primary system language.
    """
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        ensure_language_table()
        default_lang = Language.objects.filter(is_active=True, is_default=True).first()
        if not default_lang:
            default_lang = Language.objects.filter(is_active=True).first()

        if default_lang:
            serializer = LanguageSerializer(default_lang, context={'request': request})
            return Response(
                {
                    "message": "Default language retrieved successfully",
                    "data": serializer.data,
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {
                "message": "No default language found",
                "data": None
            },
            status=status.HTTP_404_NOT_FOUND
        )
