from django.contrib import admin
from unfold.admin import ModelAdmin
from .models import DeviceToken, Notification

# Device Token
@admin.register(DeviceToken)
class DeviceTokenAdmin(ModelAdmin):
    list_display = (
        'id',
        'user',
        'token',
        'device_type',
        'updated_at',
    )
    search_fields = ('token', 'device_type', 'user__email')
    ordering = ('-created_at',)




# Notification
@admin.register(Notification)
class NotificationAdmin(ModelAdmin):
    list_display = (
        'id',
        'user',
        'title',
        'notification_type',
        'created_at',
    )
    search_fields = ('title', 'notification_type', 'user__email')
    ordering = ('-created_at',)
