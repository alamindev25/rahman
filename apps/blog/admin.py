from django.contrib import admin
from .models import BlogPost, SocialLink
from unfold.admin import ModelAdmin

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
@admin.register(BlogPost)
class BlogPostAdmin(ModelAdmin):
    list_display = ('id', 'title', 'language', 'published_date')
    list_filter = ('language', 'published_date')
    search_fields = ('title', 'content', 'short_description')
    inlines = [SocialLinkInline]