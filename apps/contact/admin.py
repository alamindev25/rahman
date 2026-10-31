
# Register your models here.
from django.contrib import admin
from .models import ContactInfo, ContactMessage
from unfold.admin import ModelAdmin

@admin.register(ContactInfo)
class ContactInfoAdmin(ModelAdmin):
    list_display = ('id','email', 'phone', 'address','facebook','twitter','instagram','linkedin' )
 
@admin.register(ContactMessage)
class ContactMessageAdmin(ModelAdmin):
    list_display = ('id','full_name', 'email', 'query_type', 'created_at')
    list_filter = ('query_type', 'created_at')
    search_fields = ('full_name', 'email', 'message') 
    readonly_fields = ('created_at',) 