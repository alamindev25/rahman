from django.db.models import Avg
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny

from .models import (
    AboutBanner,
    AboutHero,
    Statistic,
    TeamMember,
    WhyChooseUs,
    MissionVision,
)
from .serializers import (
    AboutBannerSerializer,
    AboutHeroSerializer,
    StatisticSerializer,
    TeamMemberSerializer,
    WhyChooseUsSerializer,
    MissionVisionSerializer,
)
from apps.clinic.models import ClinicProfile, ClinicRating
from apps.appoinment.models import ClinicAppointment

class AboutUsAPIView(APIView):
    permission_classes = [AllowAny] 

    def get(self, request):
        banner = AboutBanner.objects.filter(is_active=True).first()
        hero = AboutHero.objects.filter(is_active=True).first()
        banner_data = AboutBannerSerializer(banner, context={"request": request}).data if banner else None
        hero_data = AboutHeroSerializer(hero, context={"request": request}).data if hero else None

        total_clinics = ClinicProfile.objects.count()
        completed_appointments = ClinicAppointment.objects.filter(status='completed').count()
        happy_patients = completed_appointments if completed_appointments > 0 else ClinicAppointment.objects.count()
        avg_rating_val = ClinicRating.objects.aggregate(Avg('rating'))['rating__avg']
        formatted_rating = f"{round(avg_rating_val, 1)}" if avg_rating_val is not None else "5.0"
        statistics = Statistic.objects.filter(is_active=True).order_by("order")
        if statistics.exists():
            statistics_data = StatisticSerializer(
                statistics,
                many=True,
                context={"request": request}
            ).data
            for stat in statistics_data:
                title_lower = stat.get("title", "").lower()
                if "clinic" in title_lower:
                    stat["value"] = f"{total_clinics}+"
                elif "patient" in title_lower or "happy" in title_lower:
                    stat["value"] = f"{happy_patients}+"
                elif "rating" in title_lower or "average" in title_lower:
                    stat["value"] = formatted_rating
        else:
            statistics_data = [
                {
                    "id": 1,
                    "title": "Partner Clinics",
                    "value": f"{total_clinics}+",
                    "order": 1
                },
                {
                    "id": 2,
                    "title": "Happy Patients",
                    "value": f"{happy_patients}+",
                    "order": 2
                },
                {
                    "id": 3,
                    "title": "Average Rating",
                    "value": formatted_rating,
                    "order": 3
                }
            ]  
        team_members = TeamMember.objects.all().order_by("order")
        why_choose_us = WhyChooseUs.objects.all()
        mission_vision = MissionVision.objects.all()
        return Response(
            {
                "banner": banner_data,
                "hero": hero_data,
                "statistics": statistics_data,
                "team_members": TeamMemberSerializer(
                    team_members,
                    many=True,
                    context={"request": request}
                ).data,
                "why_choose_us": WhyChooseUsSerializer(
                    why_choose_us,
                    many=True,
                    context={"request": request}
                ).data,
                "mission_vision": MissionVisionSerializer(
                    mission_vision,
                    many=True,
                    context={"request": request}
                ).data,
            },
            status=status.HTTP_200_OK
        )
