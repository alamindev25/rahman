from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import Language
from .views import ensure_language_table


@admin.register(Language)
class LanguageAdmin(ModelAdmin):
    list_display = ('id', 'name', 'code', 'native_name', 'direction', 'is_active', 'is_default', 'created_at')
    list_filter = ('is_active', 'is_default', 'direction')
    search_fields = ('name', 'code', 'native_name')
    list_editable = ('is_active', 'is_default')
    ordering = ('-is_default', 'name')

    fieldsets = (
        ("Language Information", {
            "fields": ("name", "native_name", "code", "direction")
        }),
        ("Settings", {
            "fields": ("is_active", "is_default")
        }),
    )

    def changelist_view(self, request, extra_context=None):
        ensure_language_table()
        return super().changelist_view(request, extra_context=extra_context)

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        ensure_language_table()
        return super().changeform_view(request, object_id=object_id, form_url=form_url, extra_context=extra_context)
