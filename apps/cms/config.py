from .models import (
    # landing
    NavigationSection, HeroSection, IntegrationSection,FeatureSection, 
    ClinicoreSection, ComplianceSection, HowItWorksSection, WatchCliniCoreSection, 
    TestimonialSection, HeroTransformSection, BlogSection, FooterSection,     
    # about_us
    AboutHeroSection, AboutMissionSection, AboutCompanySection, AboutTransformSection, AboutContactSection,  
    # pricing
    ResearchSection, FeeSection, 
    # Term & Policy
    TermSection, PolicySection, 
    #Demo 
    DemoHeroSection,
)
from .serializers import (
    # landing
    NavigationSectionSerializer, HeroSectionSerializer, IntegrationSectionSerializer, 
    FeatureSectionSerializer, ClinicoreSectionSerializer, ComplianceSectionSerializer, 
    HowItWorksSectionSerializer, WatchCliniCoreSectionSerializer, TestimonialSectionSerializer,
    HeroTransformSectionSerializer, BlogSectionSerializer, FooterSectionSerializer, 
    # about_us
    AboutHeroSectionSerializer, AboutMissionSectionSerializer, AboutCompanySectionSerializer,
    AboutTransformSectionSerializer, AboutContactSectionSerializer, 
    # pricing
    ResearchSectionSerializer, FeeSectionSerializer,
    # Term & Policy
    TermSectionSerializer, PolicySectionSerializer, 
    #Demo 
    DemoHeroSectionSerializer, 

)

PAGE_MAP = {
    "home": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "hero": (HeroSection, HeroSectionSerializer),
        "integration": (IntegrationSection, IntegrationSectionSerializer),
        "features": (FeatureSection, FeatureSectionSerializer),
        "clinicore": (ClinicoreSection, ClinicoreSectionSerializer),
        "compliance": (ComplianceSection, ComplianceSectionSerializer),
        "howitworks": (HowItWorksSection, HowItWorksSectionSerializer),
        "watchclinicore": (WatchCliniCoreSection, WatchCliniCoreSectionSerializer),
        "testimonial": (TestimonialSection, TestimonialSectionSerializer),
        "transform": (HeroTransformSection, HeroTransformSectionSerializer),
        "blog": (BlogSection, BlogSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
    },
    "about_us": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "hero": (AboutHeroSection, AboutHeroSectionSerializer),
        "mission": (AboutMissionSection, AboutMissionSectionSerializer),
        "company": (AboutCompanySection, AboutCompanySectionSerializer),
        "transform": (AboutTransformSection, AboutTransformSectionSerializer),
        "contact": (AboutContactSection, AboutContactSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
    },
    "pricing": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "research": (ResearchSection, ResearchSectionSerializer),
        "fees": (FeeSection, FeeSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
    },
    "blog": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
    },
    "resource": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
        },
    "demo": {
        "nav": (NavigationSection, NavigationSectionSerializer),
        "hero": (DemoHeroSection, DemoHeroSectionSerializer),
        "testimonial": (TestimonialSection, TestimonialSectionSerializer),
        "transform": (HeroTransformSection, HeroTransformSectionSerializer),
        "blog": (BlogSection, BlogSectionSerializer),
        "footer": (FooterSection, FooterSectionSerializer),
        }, 
    "legal": {
        "terms": (TermSection, TermSectionSerializer),
        "policy": (PolicySection, PolicySectionSerializer),
    },
}