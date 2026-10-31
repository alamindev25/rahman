from rest_framework import serializers
from apps.utils.helpers import get_url

from .models import (
    # Landing Page
    NavigationItem, NavigationSection, HeroSection, IntegrationItem, IntegrationSection,
    FeatureItem, FeatureSection, ClinicoreSection, ComplianceSection,HowItWorksItem, 
    HowItWorksSection, WatchCliniCoreSection, TestimonialItem, TestimonialSection, 
    TransformSection, BlogSection, SocialLink, FooterSection, 
    # About Us
    AboutItem, AboutHeroSection, AboutMissionSection, AboutCompanySection, 
    AboutTransformSection, AboutContactSection, AboutContactSubmission, 
    # Pricing 
    ResearchSection, ResearchItem, FeeSection, FeeItems, 
    # Term
    TermSection, PolicySection, 
    #Demo 
    DemoHeroSection, DemoHeroItem, DemoBooking,FAQ

)



'''Landing Page Section'''

# Nav Section
class NavigationItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NavigationItem
        fields = ['id', 'label']

class NavigationSectionSerializer(serializers.ModelSerializer):
    navinfo = NavigationItemSerializer(read_only=True, many=True)
    brand_logo = serializers.SerializerMethodField()
    
    class Meta:
        model = NavigationSection
        fields = [
            'id', 'brand_name', 'brand_logo', 'navinfo', 'button_text_1', 
            'button_text_2',
        ]
    def get_brand_logo(self, obj):
        return get_url(self, obj)

# Hero Section
class HeroSectionSerializer(serializers.ModelSerializer):
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()

    class Meta:
        model = HeroSection
        fields = [
            'id', 'title', 'description', 'image1', 'image2', 'image3', 'button_text_3'
    ]

    def get_image1(self, obj):
        return get_url(self, obj)

    def get_image2(self, obj):
        return get_url(self, obj)

    def get_image3(self, obj):
        return get_url(self, obj)

# Integration Section
class IntegrationItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = IntegrationItem
        fields = [
            'id', 'icon', 'name'
        ]
    def get_icon(self, obj):
        return get_url(self, obj)

class IntegrationSectionSerializer(serializers.ModelSerializer):
    integration_section = IntegrationItemSerializer(read_only=True, many=True)
    
    class Meta:
        model = IntegrationSection
        fields = [
            'id', 'title', 'integration_section', 
        ]

# Features Section
class FeatureItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = FeatureItem
        fields = [
            'id', 'icon', 'title', 'description'
        ]
        
    def get_icon(self, obj):
        return get_url(self, obj)

class FeatureSectionSerializer(serializers.ModelSerializer):
    feature_item = FeatureItemSerializer(read_only=True, many=True)
    class Meta:
        model = FeatureSection
        fields = [
            'id', 'title', 'sub_title', 'feature_item', 
        ]

# CliniCore Section
class ClinicoreSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = ClinicoreSection
        fields = [
            'id', 'title', 'sub_title', 'image'
        ]

    def get_image(self, obj):
        return get_url(self, obj)

# Compliance Section
class ComplianceSectionSerializer(serializers.ModelSerializer):
    feature_section = FeatureSectionSerializer(source="features", read_only=True)
    class Meta:
        model = ComplianceSection
        fields = [
            'id', 'feature_section'
        ]

# HowItWorks Section
class HowItWorksItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = HowItWorksItem
        fields = [
            'id', 'title', 'description'
        ]

class HowItWorksSectionSerializer(serializers.ModelSerializer):
    items = HowItWorksItemSerializer(read_only=True, many=True)
    image1 = serializers.SerializerMethodField()
    image2 = serializers.SerializerMethodField()
    image3 = serializers.SerializerMethodField()
    class Meta:
        model = HowItWorksSection
        fields = [
            'id', 'heading', 'title', 'image1', 'image2', 'image3', 'items', 'button_text'
        ]

    def get_image1(self, obj):
        return get_url(self, obj)

    def get_image2(self, obj):
        return get_url(self, obj)

    def get_image3(self, obj):
        return get_url(self, obj)

# WatchCliniCore Section
class WatchCliniCoreSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = WatchCliniCoreSection
        fields = [
            'id', 'title', 'description', 'video',
        ]

# Testimonial Section
class TestimonialItemSerializer(serializers.ModelSerializer):
    client_image = serializers.SerializerMethodField()
    class Meta:
        model = TestimonialItem
        fields = [
            'id', 'client_name', 'client_image', 'client_designation', 'message', 'order'
        ]

    def get_client_image(self, obj):
        return get_url(self, obj)

class TestimonialSectionSerializer(serializers.ModelSerializer):
    testimonial_item = TestimonialItemSerializer(read_only=True, many=True)
    class Meta:
        model = TestimonialSection
        fields = [
            'id', 'title', 'testimonial_item',
        ]

# Transform Common (landing + about_us)
class TransformSectionSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = TransformSection
        fields = [
            'id', 'heading', 'title', 'image', 'button_text_1', 'button_text_2', 
        ]

    def get_image(self, obj):
        return get_url(self, obj)

# Hero Transform Section
class HeroTransformSectionSerializer(serializers.ModelSerializer):
    transform = TransformSectionSerializer(read_only=True)
    class Meta:
        model = AboutTransformSection
        fields = [
            'id', 'transform'
        ]

# Blog Section
class BlogSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogSection
        fields = [
            'id', 'title', 'description', 'button_text', 
        ]

# Footer Section
class SocialLinkSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = SocialLink
        fields = [
            'id', 'platform', 'icon', 'url'
        ]

    def get_icon(self, obj):
        return get_url(self, obj)

class FooterSectionSerializer(serializers.ModelSerializer):
    navigationitem = NavigationItemSerializer(read_only=True, many=True)
    social_link = SocialLinkSerializer(read_only=True, many=True)
    logo = serializers.SerializerMethodField()
    class Meta:
        model = FooterSection
        fields = [
            'id', 'logo', 'title', 'description', 'navigationitem', 'privacy_policy', 'terms_service', 
            'social_link', 'copyright_text'
        ]
    
    def get_logo(self, obj):
        return get_url(self, obj)

'''About Us Section'''

# About Section
class AboutItemSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()
    class Meta:
        model = AboutItem
        fields = [
            'id', 'title', 'description', 'image'
        ]
    
    def get_image(self, obj):
        return get_url(self, obj)

# About Hero Section
class AboutHeroSectionSerializer(serializers.ModelSerializer):
    about_hero_items = AboutItemSerializer(read_only=True, many=True)
    class Meta:
        model = AboutHeroSection
        fields = [
            'id', 'heading', 'about_hero_items',
        ]

# About Mission Section
class AboutMissionSectionSerializer(serializers.ModelSerializer):
    about_mission_items = AboutItemSerializer(read_only=True, many=True)
    class Meta:
        model = AboutMissionSection
        fields = [
            'id', 'heading', 'about_mission_items',
        ]

# About Company Section
class AboutCompanySectionSerializer(serializers.ModelSerializer):
    about_company_items = AboutItemSerializer(read_only=True, many=True)
    class Meta:
        model = AboutCompanySection
        fields = [
            'id', 'heading', 'about_company_items', 'button_text',
        ]

# About Transform Section
class AboutTransformSectionSerializer(serializers.ModelSerializer):
    transform = TransformSectionSerializer(read_only=True)
    class Meta:
        model = AboutTransformSection
        fields = [
            'id', 'transform'
        ]

# Contact Section
class AboutContactSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContactSection
        fields = [
            'id', 'heading', 'title', 'button_text', 
        ]

class AboutContactSubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = AboutContactSubmission
        fields = [
            'id', 'full_name', 'email', 'message',
        ]

'''Pricing Section'''

# Research Section
class ResearchItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = ResearchItem
        fields = [
            'id', 'icon', 'title',
        ]

class ResearchSectionSerializer(serializers.ModelSerializer):
    research_items = ResearchItemSerializer(read_only=True, many=True)
    class Meta:
        model = ResearchSection
        fields = [
            'id', 'title', 'description', 'research_items',
        ]

# Fees Section
class FeeItemsSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeeItems
        fields = [
            'id', 'item'
        ]

class FeeSectionSerializer(serializers.ModelSerializer):
    fee_items = FeeItemsSerializer(read_only=True, many=True)
    image = serializers.SerializerMethodField()
    class Meta:
        model = FeeSection
        fields = [
            'id', 'title', 'image', 'fee_items', 
        ]
    
    def get_image(self, obj):
        return get_url(self, obj)

'''Legal Doc Section'''
class TermSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = TermSection
        fields = [
            'id', 'title', 'last_updated', 'content',
        ]

class PolicySectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicySection
        fields = [
            'id', 'title', 'last_updated', 'content',
        ]

'''Demo Section'''

# Demo Hero Section
class DemoHeroItemSerializer(serializers.ModelSerializer):
    icon = serializers.SerializerMethodField()
    class Meta:
        model = DemoHeroItem
        fields = [
            'id', 'icon', 'label'
        ]

    def get_icon(self, obj):
        return get_url(self, obj)

class DemoHeroSectionSerializer(serializers.ModelSerializer):
    hero_items = DemoHeroItemSerializer(read_only=True, many=True)
    class Meta:
        model = DemoHeroSection
        fields= [
            'id', 'heading', 'title', 'sub_title', 'hero_items',
        ]
      
class DemoBookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = DemoBooking
        fields = [
            'id', 'first_name', 'last_name', 'work_email', 'use_cases', 'topics_of_interest', 'submitted_at',
        ]

class FAQSerializer(serializers.ModelSerializer):
    class Meta:
        model = FAQ
        fields = ['id', 'question', 'answer', 'status']