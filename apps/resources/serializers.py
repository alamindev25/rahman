from rest_framework import serializers
from .models import ResourceItem, PlanningChecklist


class PlanningChecklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanningChecklist
        fields = [
            "id",
            "title",
            "order",
        ]
class ResourceItemSerializer(serializers.ModelSerializer):
    resource_type_display = serializers.CharField(source="get_resource_type_display", read_only=True)

    class Meta:
        model = ResourceItem
        fields = [
            "id",
            "resource_type",
            "resource_type_display",
            "title",
            "sub_title",
            "description",
            "icon_image",
            "is_highlighted",
            "order",
        ]


class ResourceItemDetailsSerializer(serializers.ModelSerializer):
    resource_type_display = serializers.CharField(source="get_resource_type_display", read_only=True)
    checklists = PlanningChecklistSerializer(many=True, read_only=True)

    class Meta:
        model = ResourceItem
        fields = [
            "id",
            "resource_type",
            "resource_type_display",
            "title",
            "sub_title",
            "description",
            "icon_image",
            "is_highlighted",
            "order",
            "checklists",
        ]


