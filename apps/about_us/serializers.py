
from rest_framework import serializers

from .models import (
    Statistic,
    TeamMember,
    WhyChooseUs,
    MissionVision,
    AboutBanner,
    AboutHero,
)

class AboutBannerSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutBanner
        fields = [
            "id",
            "badge",
            "title",
            "subtitle",
            "image",
            "is_active",
        ]
class AboutHeroSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutHero
        fields = [
            "id",
            "badge",
            "title",
            "description",
            "button_text",
            "button_url",
            "image",
            "secondary_image",
            "badge_text",
            "is_active",
        ]
class StatisticSerializer(serializers.ModelSerializer):
    class Meta:
        model = Statistic
        fields = [
            "id",
            "title",
            "value",
            "order",
        ]
class TeamMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = [
            "id",
            "name",
            "role",
            "image",
            "order",
        ]
class WhyChooseUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WhyChooseUs
        fields = [
            "id",
            "title",
            "description",
            "icon_class",
        ]
class MissionVisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = MissionVision
        fields = [
            "id",
            "title",
            "description",
            "image",
            "section_type",
        ]