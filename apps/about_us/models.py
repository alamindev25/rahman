from django.db import models


class AboutBanner(models.Model):
    badge = models.CharField(max_length=150, default="No. 1 Platform for Dialysis Booking", blank=True, null=True)
    title = models.CharField(max_length=255, default="Supporting Your Health Journey Worldwide")
    subtitle = models.CharField(max_length=255, default="Trusted clinics, easy booking, global reach", blank=True, null=True)
    image = models.ImageField(upload_to="about_us/banner/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "About Us Top Banner"
        verbose_name_plural = "About Us Top Banner"

    def __str__(self):
        return self.title

class AboutHero(models.Model):
    badge = models.CharField(max_length=100, default="About Us", blank=True, null=True)
    title = models.CharField(max_length=255, default="Safe, Simple, and Global Dialysis Booking")
    description = models.TextField(
        blank=True,
        null=True,
        default="We believe that travel should never be limited by health conditions. Our platform connects patients with certified dialysis clinics around the world, making it easy to compare services, check real-time availability, and book appointments with confidence. Whether you're traveling for business, vacation, or family reasons your care is always within reach."
    )
    button_text = models.CharField(max_length=100, default="Learn More", blank=True, null=True)
    button_url = models.CharField(max_length=255, default="#", blank=True, null=True)
    image = models.ImageField(upload_to="about_us/hero/", blank=True, null=True)
    secondary_image = models.ImageField(upload_to="about_us/hero/", blank=True, null=True)
    badge_text = models.CharField(max_length=150, default="High Quality Professionals", blank=True, null=True)
    is_active = models.BooleanField(default=True)
    class Meta:
        verbose_name = "About Us Hero Section"
        verbose_name_plural = "About Us Hero Section"

class Statistic(models.Model):
    title = models.CharField(max_length=100)
    value = models.CharField(max_length=50)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
    def __str__(self):
        return f"{self.title} - {self.value}"

class TeamMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    image = models.ImageField(upload_to="team/", blank=True, null=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]
    def __str__(self):
        return self.name

class WhyChooseUs(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    icon_class = models.FileField(
        max_length=100,
        blank=True,
        null=True,
    )
    order = models.PositiveIntegerField(default=0)
    image=models.ImageField(upload_to="why_choose_us/", blank=True, null=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return self.title

class MissionVision(models.Model):
    TYPE_CHOICES = [
        ("mission", "Mission"),
        ("vision", "Vision"),
    ]
    title = models.CharField(max_length=150)
    description = models.TextField()
    image = models.ImageField(upload_to="mission_vision/", blank=True, null=True)
    section_type = models.CharField(
        max_length=20,
        choices=TYPE_CHOICES,
        unique=True
    )

    def __str__(self):
        return self.title