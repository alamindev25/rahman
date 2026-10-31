from django.db import models

# Create your models here.
class ResourceItem(models.Model):
    class ResourceType(models.TextChoices):
        BOOK_DIALYSIS_ABROAD = "book_dialysis_abroad", "Book Dialysis Abroad"
        HOLIDAY_DESTINATIONS = "holiday_destinations", "Holiday Destinations"
        TRAVEL_INSURANCE = "travel_insurance", "Travel Insurance"
        CRUISE_DIALYSIS = "cruise_dialysis", "Cruise Dialysis"
        DIALYSIS_AT_SEA = "dialysis_at_sea", "Dialysis at Sea"
        PATIENT_GUIDES = "patient_guides", "Patient Guides"
        BENEFITS_FINANCIAL_HELP = "benefits_financial_help", "Benefits & Financial Help"
        KIDNEY_DIET = "kidney_diet", "Kidney Diet"
        TRAVEL_TIPS = "travel_tips", "Travel Tips"
        
        # FAQS = "faqs", "FAQs"

    resource_type = models.CharField(
        max_length=50,
        choices=ResourceType.choices,
        blank=True,
        null=True,
        help_text="Select design resource type"
    )
    title = models.CharField(max_length=200)
    sub_title = models.CharField(max_length=200, null=True, blank=True)    
    description = models.TextField()
    icon_image = models.ImageField(upload_to='icons/', blank=True, null=True)
    is_highlighted = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order"]

    def __str__(self):
        return f"{self.title}"

        
class PlanningChecklist(models.Model):
    resource = models.ForeignKey(
        ResourceItem, 
        on_delete=models.CASCADE, 
        related_name="checklists"
    ) 
    title = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)
    class Meta:
        ordering = ["order"]
        verbose_name ="Planning Checklist"
        verbose_name_plural = "Planning Checklists"
    def __str__(self):
        return self.title
