from django.contrib import admin
from django.utils.html import format_html
from unfold.admin import ModelAdmin, TabularInline
from .models import ResourceItem, PlanningChecklist


class PlanningChecklistInline(TabularInline):
    model = PlanningChecklist
    extra = 1


@admin.register(ResourceItem)
class ResourceItemAdmin(ModelAdmin):
    list_display = ("order", "icon_preview", "title", "resource_type", "sub_title", "is_highlighted")
    list_display_links = ("title",)
    list_editable = ("is_highlighted", "order")
    # list_filter = ("resource_type", "is_highlighted")
    search_fields = ("title", "sub_title", "description")
    inlines = [PlanningChecklistInline]

    def icon_preview(self, obj):
        if obj.icon_image:
            return format_html(
                '<img src="{}" style="width: 32px; height: 32px; object-fit: contain; background: #e0f2fe; border-radius: 50%; padding: 2px;" />',
                obj.icon_image.url,
            )
        return "-"
    icon_preview.short_description = "Icon"


@admin.register(PlanningChecklist)
class PlanningChecklistAdmin(ModelAdmin):
    list_display = ("title", "resource", "order")
    list_editable = ("order",)
    search_fields = ("title",)

