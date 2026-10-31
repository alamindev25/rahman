from django.contrib import admin
from apps.cms.models import CMS, FAQ, Page
from unfold.admin import ModelAdmin
from django.contrib import admin
import nested_admin
from unfold.admin import ModelAdmin, TabularInline
from apps.utils.helpers import admin_image_preview, admin_video_preview

from .models import (
    # landing
    NavigationItem, NavigationSection, HeroSection, IntegrationItem, IntegrationSection,
    FeatureItem, FeatureSection, ClinicoreSection, ComplianceSection,HowItWorksItem, 
    HowItWorksSection, WatchCliniCoreSection, TestimonialItem, TestimonialSection, 
    HeroTransformSection, TransformSection, BlogSection, SocialLink, FooterSection, 
    AboutItem, AboutHeroSection, AboutMissionSection, AboutCompanySection, 
    AboutTransformSection, AboutContactSection, AboutContactSubmission, 
    ResearchSection, ResearchItem, FeeSection,
    FeeItems, 
    TermSection, PolicySection, 
    DemoHeroSection, DemoHeroItem, DemoBooking

)
# Nav Section
class NavigationItemInline(TabularInline):
    model = NavigationItem
    extra = 1
    fields = ('label',)

@admin.register(NavigationSection)
class NavigationSectionAdmin(ModelAdmin):
    list_display = ('id', 'brand_logo_preview', 'brand_name', 'created_at', 'updated_at')
    inlines = [NavigationItemInline]
    readonly_fields = ('brand_logo_preview',)

    def brand_logo_preview(self, obj):
        return admin_image_preview(obj, 'brand_logo')
    brand_logo_preview.short_description = "Logo"

# Hero Section
@admin.register(HeroSection)
class HeroSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'image1_preview', 'image2_preview', 'image3_preview', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('image1_preview', 'image2_preview', 'image3_preview')

    def image1_preview(self, obj):
        return admin_image_preview(obj, 'image1')
    image1_preview.short_description = "Image 1"

    def image2_preview(self, obj):
        return admin_image_preview(obj, 'image2')
    image2_preview.short_description = "Image 2"

    def image3_preview(self, obj):
        return admin_image_preview(obj  , 'image3')
    image3_preview.short_description = "Image 3"

# Integration Section
class IntegrationItemInline(TabularInline):
    model = IntegrationItem
    extra = 1
    fields = ('icon', 'icon_preview', 'name')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return admin_image_preview(obj, 'icon', height=30)
    icon_preview.short_description = "Preview"

@admin.register(IntegrationSection)
class IntegrationSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    inlines = [IntegrationItemInline]
    search_fields = ('title',)

# Features Section
class FeatureItemInline(TabularInline):
    model = FeatureItem
    extra = 1
    fields = ('icon', 'title', 'description')

@admin.register(FeatureSection)
class FeatureSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    inlines = [FeatureItemInline]

#CliniCore Section
@admin.register(ClinicoreSection)
class ClinicoreSectionAdmin(ModelAdmin):
    list_display = ('id', 'image_preview', 'title', 'created_at', 'updated_at')
    search_fields = ('id',)
    ordering = ('id',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return admin_image_preview(obj, 'image', height=40)
    image_preview.short_description = "Image"

# Compliance Section
admin.site.register(ComplianceSection)

# HowItWorks Section
class HowItWorksItemInline(TabularInline):
    model = HowItWorksItem
    extra = 1
    fields = ('title', 'description')

@admin.register(HowItWorksSection)
class HowItWorksSectionAdmin(ModelAdmin):
    list_display = ('id', 'heading', 'title', 'created_at', 'updated_at')
    inlines = [HowItWorksItemInline]
    search_fields = ('title',)

    readonly_fields = ('image1_preview', 'image2_preview', 'image3_preview')

    def image1_preview(self, obj):
        return admin_image_preview(obj, 'image1')
    image1_preview.short_description = "Image 1"

    def image2_preview(self, obj):
        return admin_image_preview(obj, 'image2')
    image2_preview.short_description = "Image 2"

    def image3_preview(self, obj):
        return admin_image_preview(obj, 'image3')
    image3_preview.short_description = "Image 3"

# WatchCliniCore Section
@admin.register(WatchCliniCoreSection)
class WatchCliniCoreSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    readonly_fields = ('video_preview',)

    def video_preview(self, obj):
        return admin_video_preview(obj, 'video_thumbnail')
    video_preview.short_description = "Video Thumbnail"

# Testimonial Section
class TestimonialItemInline(TabularInline):
    model = TestimonialItem
    extra = 1
    fields = ('client_name', 'client_image_preview', 'client_image', 'client_designation', 'message', 'order')
    readonly_fields = ('client_image_preview',)

    def client_image_preview(self, obj):
        return admin_image_preview(obj, 'client_image', height=30)
    client_image_preview.short_description = "Client Image Preview"

@admin.register(TestimonialSection)
class TestimonialSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    inlines = [TestimonialItemInline]
    search_fields = ('title',)

# Transform Section
admin.site.register(TransformSection)
admin.site.register(HeroTransformSection)

# Blog Section
@   admin.register(BlogSection)
class BlogSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('id',)

# Footer Section
class SocialLinkInline(TabularInline):
    model = SocialLink
    extra = 1
    fields = ('platform', 'icon', 'url')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return admin_image_preview(obj, 'icon', height=25)
    icon_preview.short_description = "Icon Preview"

@admin.register(FooterSection)
class FooterSectionAdmin(ModelAdmin):
    list_display = ('id', 'created_at', 'updated_at')
    inlines = [SocialLinkInline]
    ordering = ('id',)

'''About Us Section'''

# About Hero Section
class AboutItemInline(TabularInline):
    model = AboutItem
    extra = 1
    fields = ('title', 'description', 'image', 'image_preview')
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return admin_image_preview(obj, 'image', height=40)
    image_preview.short_description = "Image Preview"

@admin.register(AboutHeroSection)
class AboutHeroSectionAdmin(ModelAdmin):
    list_display = ('id', 'heading', 'created_at', 'updated_at')
    inlines = [AboutItemInline]
    search_fields = ('heading',)
    ordering = ('id',)

# About Mission Section
@admin.register(AboutMissionSection)
class AboutMissionSectionAdmin(ModelAdmin):
    list_display = ('id', 'heading', 'created_at', 'updated_at')
    inlines = [AboutItemInline]
    search_fields = ('heading',)
    ordering = ('id',)

# About Company Section
@admin.register(AboutCompanySection)
class AboutCompanySectionAdmin(ModelAdmin):
    list_display = ('id', 'heading', 'created_at', 'updated_at')
    inlines = [AboutItemInline]
    search_fields = ('heading',)
    ordering = ('id',)

# About Transform Section
admin.site.register(AboutTransformSection)

# About Contact Section
@admin.register(AboutContactSection)
class AboutContactSectionAdmin(ModelAdmin):
    list_display = ('id', 'heading', 'created_at', 'updated_at')
    search_fields = ('heading',)
    ordering = ('id',)

admin.site.register(AboutContactSubmission)

# Research Section
class ResearchItemInline(TabularInline):
    model = ResearchItem
    extra = 1
    fields = ('icon_preview', 'icon', 'title')
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return admin_image_preview(obj, 'icon', height=30)
    icon_preview.short_description = "Preview"

@admin.register(ResearchSection)
class ResearchSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('id',)
    inlines = [ResearchItemInline]

# Fees Section
class FeeItemsInline(TabularInline):
    model = FeeItems
    extra = 1
    fields = ('item',)
    ordering = ('id',)

@admin.register(FeeSection)
class FeeSectionAdmin(ModelAdmin):
    list_display = ('id', 'image_preview', 'title', 'created_at', 'updated_at')
    search_fields = ('title',)
    ordering = ('id',)
    inlines = [FeeItemsInline]
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        return admin_image_preview(obj, 'image', height=40)
    image_preview.short_description = "Preview"

'''Legal Doc Section'''

@admin.register(TermSection)
class TermSectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'last_updated')
    search_fields = ('title',)
    list_filter = ('last_updated', 'created_at')

@admin.register(PolicySection)
class PolicySectionAdmin(ModelAdmin):
    list_display = ('id', 'title', 'last_updated')
    search_fields = ('title',)
    list_filter = ('last_updated', 'created_at')

'''Demo Section'''

# Demo Hero Section
class DemoHeroItemInline(TabularInline):
    model = DemoHeroItem
    extra   = 1
    fields = ('icon', 'icon_preview', 'label',)
    readonly_fields = ('icon_preview',)

    def icon_preview(self, obj):
        return admin_image_preview(obj, 'icon', height=40)
    icon_preview.short_description = "Preview"

@admin.register(DemoHeroSection)
class DemoHeroSectionAdmin(ModelAdmin):
    list_display = ('id', 'heading',)
    inlines = [DemoHeroItemInline]
    search_fields = ('title',)
    list_filter = ('created_at', )

@admin.register(DemoBooking)
class DemoBookingAdmin(ModelAdmin):
    list_display = ('id', 'first_name', 'work_email')
    search_fields = ('work_email',)
    list_filter = ('submitted_at',)



# Default
@admin.register(Page)
class CustomAdminClass(ModelAdmin):
    list_display = ('id', 'title','content')
    list_display_links = ('id', 'title','content')

    fieldsets = (
        (None, {
            'fields': ('title', 'content', 'type', 'status')
        }),
    )

@admin.register(CMS)
class CMSAdmin(ModelAdmin):
    pass

@admin.register(FAQ)
class FAQAdmin(ModelAdmin):
    list_display = ('id', 'question', 'status')
    list_display_links = ('id', 'question')

    fieldsets = (
        (None, {
            'fields': ('question', 'answer', 'status')
        }),
    )