from rest_framework import serializers
from .models import BlogPost, SocialLink
from apps.language.serializers import LanguageSerializer


class SocialLinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = SocialLink
        fields = ['platform_name', 'link']

class BlogPostSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)
    language_code = serializers.CharField(source='language.code', read_only=True, default='en')
    language_name = serializers.CharField(source='language.name', read_only=True, default='English')
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'language',
            'language_code',
            'language_name',
            'title',
            'image',
            'image_url',
            'short_description',
            'content',
            'published_date',
            'social_links'
        ]
        extra_kwargs = {
            'image': {'write_only': True}
        } 
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            file_url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(file_url)
            return file_url
        return None

class BlogPostListSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()
    social_links = SocialLinkSerializer(many=True, read_only=True)
    language_code = serializers.CharField(source='language.code', read_only=True, default='en')
    language_name = serializers.CharField(source='language.name', read_only=True, default='English')
    class Meta:
        model = BlogPost
        fields = [
            'id',
            'language',
            'language_code',
            'language_name',
            'title',
            'image',
            'image_url',
            'short_description',
            'published_date',
            'social_links'
        ]
        extra_kwargs = {
            'image': {'write_only': True}
        }
    
    def get_image_url(self, obj):
        request = self.context.get('request')
        if obj.image and hasattr(obj.image, 'url'):
            file_url = obj.image.url
            if request is not None:
                return request.build_absolute_uri(file_url)
            return file_url
        return None
        