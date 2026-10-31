from django.db import models


class Language(models.Model):
    DIRECTION_CHOICES = [
        ('ltr', 'Left to Right'),
        ('rtl', 'Right to Left'),
    ]

    code = models.CharField(max_length=10, unique=True, help_text="e.g. en, zh-hans, hi, es, fr, ru, ur, id, bn")
    name = models.CharField(max_length=100, help_text="English name of the language")
    native_name = models.CharField(max_length=100, blank=True, help_text="Native name e.g. Español, বাংলা, हिंदी")
    direction = models.CharField(max_length=3, choices=DIRECTION_CHOICES, default='ltr')
    is_active = models.BooleanField(default=True)
    is_default = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "Language"
        verbose_name_plural = "Languages"

    def __str__(self):
        return f"{self.name} ({self.code})"