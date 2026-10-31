from django.db import models
from django.utils.text import slugify
from django.db import models
from django_ckeditor_5.fields import CKEditor5Field
from django.contrib.postgres.fields import ArrayField

'''Landing Page Section'''

# Nav Section
class NavigationSection(models.Model):
    brand_name = models.CharField(max_length=100, default="Figgle", null=True, blank=True)
    brand_logo = models.ImageField(upload_to="brand_logos/", blank=True, null=True)
    button_text_1 = models.CharField(max_length=50, default="Book Demo", null=True, blank=True)
    button_text_2 = models.CharField(max_length=50, default="Login", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.brand_name or "Nav Section"

class NavigationItem(models.Model):
    navigation_section = models.ForeignKey(NavigationSection, related_name="navinfo", on_delete=models.CASCADE, blank=True)
    label = models.CharField(max_length=100, help_text="Menu name (e.g., Home, About Us, Pricing)", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.label or "Navigation Item"

# Hero Section
class HeroSection(models.Model):
    title = models.CharField(max_length=255, default="Easy, Simple, and Flexible - Your Research Partner", null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="Operate EDC, Research Notes, and R/AI Analysis seamlessly under one account, and stay compliant with regulations (21 CFR Part 11, eIDAS, GDPR).")
    image1 = models.ImageField(upload_to="hero_images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="hero_images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="hero_images/", null=True, blank=True)
    button_text_3 = models.CharField(max_length=50, default="Get Early Access", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Hero Section"

# Integration Section
class IntegrationSection(models.Model):
    title = models.CharField(max_length=255, default="Integrated with the top customer engagement apps...", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class IntegrationItem(models.Model):
    integration_section = models.ForeignKey(IntegrationSection, related_name="icons", on_delete=models.CASCADE, blank=True)
    icon = models.ImageField(upload_to="integration_icons/", null=True, blank=True)
    name = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name or "Integration Section"

# Features Section
class FeatureSection(models.Model):
    title = models.CharField(max_length=100, null=True, blank=True)
    sub_title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Features Section"

class FeatureItem(models.Model):
    feature_section = models.ForeignKey(FeatureSection, related_name="feature_item", on_delete=models.CASCADE, blank=True)
    icon = models.ImageField(upload_to="feature_icons/", null=True, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title or "Feature Items"

#CliniCore Section
class ClinicoreSection(models.Model):
    title = models.CharField(max_length=255, default="Meet CliniCore", null=True, blank=True)
    sub_title = models.TextField(default="Your plug and play clinical research platform.", null=True, blank=True)
    image = models.ImageField(upload_to="clinicore_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "CliniCore Section"

# Compliance Section
class ComplianceSection(models.Model):
    features = models.ForeignKey(FeatureSection, on_delete=models.CASCADE, related_name="compliance", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.features.title or "Compliance Section"

# HowItWorks Section
class HowItWorksSection(models.Model):
    heading = models.CharField(max_length=255, default="How does it work?", null=True, blank=True)
    title = models.CharField(max_length=255, default="A CliniCore you can trust", null=True, blank=True)
    image1 = models.ImageField(upload_to="how_it_works_images/", null=True, blank=True)
    image2 = models.ImageField(upload_to="how_it_works_images/", null=True, blank=True)
    image3 = models.ImageField(upload_to="how_it_works_images/", null=True, blank=True)
    button_text = models.CharField(max_length=50, default="Create My Project Now", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "How It Works Section"

class HowItWorksItem(models.Model):
    how_it_works_section = models.ForeignKey(HowItWorksSection, related_name="items", on_delete=models.CASCADE, blank=True)
    title = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or "How It Works Item"

# WatchCliniCore Section
class WatchCliniCoreSection(models.Model):
    title = models.CharField(max_length=255, default="Watch CliniCore in action", null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="See how our  clinical research platform automates data gathering across your apps to help your marketing team get access to data and insights to make decisions quickly ")
    video = models.FileField(upload_to='videos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Watch CliniCore Section"

# Testimonial Section
class TestimonialSection(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Testimonial Section"

class TestimonialItem(models.Model):
    testimonial_section = models.ForeignKey(TestimonialSection, related_name='testimonial_item', on_delete=models.CASCADE, blank=True)
    client_name = models.CharField(max_length=255, null=True, blank=True)
    client_image = models.ImageField(upload_to="testimonial_images/", null=True, blank=True)
    client_designation = models.CharField(max_length=255, null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    order = models.PositiveBigIntegerField(default=0, help_text="Order in Slider")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.client_name or "Testimonial Item"

# Transform Common (landing + about_us)
class TransformSection(models.Model):
    heading = models.CharField(max_length=255, default="Try CliniCore Today", null=True, blank=True)
    title = models.TextField(null=True, blank=True, default="Ready to Transform Your Clinical Research?")
    image = models.ImageField(upload_to="transform_images/", null=True, blank=True)
    button_text_1 = models.CharField(max_length=255, default="Get Started", null=True, blank=True)
    button_text_2 = models.CharField(max_length=255, default="Book Demo", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading or "Transform Section"

# Hero Transform Section
class HeroTransformSection(models.Model):
    transform = models.ForeignKey(TransformSection, on_delete=models.CASCADE, related_name="hero_transform", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transform.heading if self.transform else "Hero Transform Section"

# Blog Section
class BlogSection(models.Model):
    title = models.CharField(max_length=255, default="Blog Post", null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    button_text = models.CharField(max_length=255, default="See All", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Blog Section"

# Footer Section
class FooterSection(models.Model):
    logo = models.ImageField(upload_to="footer_logos/", null=True, blank=True)
    title = models.CharField(max_length=255, default="CliniCore", null=True, blank=True)
    description = models.TextField(null=True, blank=True, default="Clinical Research Platfrom")
    navigationitem = models.ManyToManyField(NavigationItem, related_name="nav", blank=True) # Home, Pricing, Features
    privacy_policy = models.CharField(max_length=255, default="Privacy Policy", null=True, blank=True)
    terms_service = models.CharField(max_length=255, default="Terms & Conditions", null=True, blank=True)
    copyright_text = models.CharField(max_length=200, default="© CliniCore. All Rights Reserved.", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Footer Section"

class SocialLink(models.Model):
    footersection = models.ForeignKey(FooterSection, related_name="social_links", on_delete=models.CASCADE, blank=True) # facebook instagram, linkedin
    platform = models.CharField(max_length=50, null=True, blank=True)  # Instagram, LinkedIn
    icon = models.ImageField(upload_to="social_icons/", null=True, blank=True)  # store icon name/class
    url = models.URLField(null=True, blank=True) # link to social media
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.platform or "Social Platform"

'''About Us Section'''

# About Hero Section
class AboutHeroSection(models.Model):
    heading = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading if self.heading else "About Hero Section"

# About Mission Section
class AboutMissionSection(models.Model):
    heading = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading if self.heading else "About Mission Section"

# About Company Section
class AboutCompanySection(models.Model):
    heading = models.CharField(max_length=255, null=True, blank=True)
    button_text = models.CharField(max_length=255, default="Read More", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.heading if self.heading else "About Company Section"

class AboutItem(models.Model):
    about_hero = models.ForeignKey(AboutHeroSection, on_delete=models.CASCADE, related_name="about_hero_items", blank=True, null=True)
    about_mission = models.ForeignKey(AboutMissionSection, on_delete=models.CASCADE, related_name="about_mission_items", blank=True, null=True)
    about_company = models.ForeignKey(AboutCompanySection, on_delete=models.CASCADE, related_name="about_company_items", blank=True, null=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True) 
    image = models.ImageField(upload_to="about_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title or "About Item Section"

# About Transform Section
class AboutTransformSection(models.Model):
    transform = models.ForeignKey(TransformSection, on_delete=models.CASCADE, related_name="about_transform", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.transform.heading if self.transform else "About Transform Section"

# About Contact Section
class AboutContactSection(models.Model):
    heading = models.CharField(max_length=255, default="Contact Us Form", null=True, blank=True)
    title = models.CharField(max_length=255, default="For more information about our comoany or ifthere any question please contact us", null=True, blank=True)
    button_text = models.CharField(max_length=255, default="Submit", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.title or "Contact Section"

class AboutContactSubmission(models.Model):

    full_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)
    submitted_at = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.full_name} - {self.email}" if self.full_name else "Contact Submission"
        
# Research Section
class ResearchSection(models.Model):
    title = models.CharField(max_length=255, default="Start clinical research in Seconds", null=True, blank=True)
    description = models.TextField(default="Rent collection is our flagship product customers love it because it is fast, easy and secure", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Research Section"

class ResearchItem(models.Model):
    research_section = models.ForeignKey(ResearchSection, on_delete=models.CASCADE, related_name="research_items", null=True, blank=True)
    icon = models.ImageField(upload_to="research_icons/", null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Research Item"

# Fees Section
class FeeSection(models.Model):
    title = models.CharField(max_length=255, default="Fees we DON’T charge", null=True, blank=True)
    image = models.ImageField(upload_to="fee_images/", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Fees Section"

class FeeItems(models.Model):
    fee_section = models.ForeignKey(FeeSection, max_length=255, on_delete=models.CASCADE, related_name="fee_items", null=True, blank=True)
    item = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.item or "Fee Items"

'''Legal Doc Section'''

class TermSection(models.Model):
    title = models.CharField(max_length=255, default="Terms and Conditions", null=True, blank=True)
    last_updated = models.DateField()
    content = CKEditor5Field('Content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title or "Term Section"

class PolicySection(models.Model):
    title = models.CharField(max_length=255, default="Privacy Policy", null=True, blank=True)
    last_updated = models.DateField()
    content = CKEditor5Field('Content')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self else "Policy Section"

'''Demo Section'''

# Demo Hero Section
class DemoHeroSection(models.Model):
    heading = models.CharField(max_length=255, default="BOOK A DEMO", null=True, blank=True)
    title = models.CharField(max_length=255, default="Speak with an expert", null=True, blank=True)
    sub_title = models.CharField(max_length=255, default="Our team can help you:", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title if self.title else "Demo Hero Section"

class DemoHeroItem(models.Model):
    demo_hero_section = models.ForeignKey(DemoHeroSection, on_delete=models.CASCADE, related_name="hero_items", null=True, blank=True)
    icon = models.ImageField(upload_to="demo_hero_icons/", null=True, blank=True)
    label = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return self.label if self.label else "Demo Hero Item"

class DemoBooking(models.Model):
    USE_CASE_CHOICES = [
        ('edc', 'EDC + eCRF Builder'),
        ('eln', 'Research Notes (ELN)'),
        ('r_ai', 'R / AI Analysis'),
    ]
    first_name = models.CharField(max_length=100, null=True, blank=True)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    work_email = models.EmailField(null=True, blank=True)
    use_cases = models.JSONField(models.CharField(max_length=20, choices=USE_CASE_CHOICES), blank=True, null=True)
    topics_of_interest = models.TextField(blank=True, null=True)
    submitted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name}-{self.work_email}"

# Default
class Page(models.Model):

    class Type(models.TextChoices):
        PRIVACY_POLICY = 'privacy_policy', 'Privacy Policy'
        TERMS_AND_CONDITIONS = 'terms_and_conditions', 'Terms and Conditions'
        COOKIE_POLICY = 'cookie_policy', 'Cookie Policy'
        IMPRINT = 'imprint', 'Imprint'

    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    content = models.TextField()
    type = models.CharField(max_length=50, choices=Type.choices)
    status = models.BooleanField(default=True)
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} (v{self.version})"

class CMS(models.Model):
    page = models.CharField(max_length=255, blank=True, null=True)
    section = models.CharField(max_length=255, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    sub_title = models.TextField(blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    background_image = models.CharField(max_length=255, blank=True, null=True)
    file_url = models.CharField(max_length=255, blank=True, null=True)
    button_text = models.CharField(max_length=255, blank=True, null=True)
    button_link = models.CharField(max_length=255, blank=True, null=True)
    other = models.CharField(max_length=255, blank=True, null=True)
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    ]
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='active'
    )
    def __str__(self):
        return self.title or 'Page'

class FAQ(models.Model):
    question = models.CharField(max_length=255)
    answer = models.TextField()
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.question