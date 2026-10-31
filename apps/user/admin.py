from django.contrib import admin
from django.utils.html import format_html
from django.utils.translation import gettext_lazy as _
from unfold.admin import ModelAdmin


from .models import User, UserProfile
from apps.clinic.models import ClinicRegister

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = _('Associated Profile Data Matrix')

@admin.register(User)
class CustomAdminClass(ModelAdmin):
   
    list_display = ('id', 'email', 'role', 'preview_user_image', 'check_is_superuser', 'is_verified')
    list_display_links = ('id', 'email', 'preview_user_image', 'check_is_superuser')
    list_filter = ('role', 'is_verified', 'is_staff', 'is_superuser')
    search_fields = ('id', 'email', 'user_profile__first_name', 'user_profile__last_name')
    inlines = (UserProfileInline,)

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.exclude(id=1)

    @admin.display(description=_('User Avatar'))
    def preview_user_image(self, obj):
        if obj.avatar:
            return format_html('<img src="{}" style="height: 35px; width: 35px; border-radius: 50%; object-fit: cover;" />', obj.avatar.url)
        return format_html('<span style="color: #9ca3af;">No Image</span>')
    
    @admin.display(description=_('Is Superuser'))
    def check_is_superuser(self, obj):
        return 'YES' if obj.is_superuser else 'NO'
@admin.register(UserProfile)

class Useruser_profileAdmin(ModelAdmin):
    list_display = ('id', 'user', 'first_name', 'last_name', 'phone', 'dob')
    list_display_links = ('id', 'user', 'first_name', 'last_name')
    search_fields = ('user__email', 'first_name', 'last_name')


