from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.shortcuts import get_object_or_404
from django.db.models import Q
from .models import BlogPost
from .serializers import BlogPostSerializer, BlogPostListSerializer
from rest_framework.permissions import AllowAny

class BlogPostListAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request):
        lang_code = request.GET.get('lang') or request.GET.get('Accept-Language') or getattr(request, 'LANGUAGE_CODE', 'en')
        if lang_code:
            lang_code = lang_code.lower()
        blogs = BlogPost.objects.filter(
            Q(language__code=lang_code) | Q(language__isnull=True)
        ).order_by('-published_date')
        if not blogs.exists():
            blogs = BlogPost.objects.filter(
                Q(language__code='en') | Q(language__isnull=True)
            ).order_by('-published_date')
        if not blogs.exists():
            blogs = BlogPost.objects.all().order_by('-published_date')
        serializer = BlogPostListSerializer(blogs, many=True, context={'request': request})
        return Response(
            {
                "message": "Blog list retrieved successfully",
                "requested_language": lang_code,
                "count": blogs.count(),
                "data": serializer.data,
            },
            status=status.HTTP_200_OK
        )
    
class BlogPostDetailAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    def get(self, request, pk):
        blog = get_object_or_404(BlogPost, pk=pk)
        blog_serializer = BlogPostSerializer(blog, context={'request': request})
        return Response(
            {
                "message": "Blog detail retrieved successfully",
                "blog_detail": blog_serializer.data,
            },
            status=status.HTTP_200_OK
        )