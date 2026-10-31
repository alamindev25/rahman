from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import AboutBanner, AboutHero, Statistic, TeamMember, WhyChooseUs, MissionVision


@admin.register(AboutBanner)
class AboutBannerAdmin(ModelAdmin):
    list_display = ("title", "badge", "is_active")
    list_editable = ("is_active",)


@admin.register(AboutHero)
class AboutHeroAdmin(ModelAdmin):
    list_display = ("title", "badge", "is_active")
    list_editable = ("is_active",)


@admin.register(Statistic)
class StatisticAdmin(ModelAdmin):
    list_display = ("title", "value", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "value")


@admin.register(TeamMember)
class TeamMemberAdmin(ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role")


@admin.register(WhyChooseUs)
class WhyChooseUsAdmin(ModelAdmin):
    list_display = ("title", "icon_class", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("title", "description")


@admin.register(MissionVision)
class MissionVisionAdmin(ModelAdmin):
    list_display = ("title", "section_type")
    search_fields = ("title", "description")


