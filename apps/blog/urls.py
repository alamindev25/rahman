from django.urls import path
from .views import BlogPostDetailAPIView,BlogPostListAPIView


urlpatterns = [
    path('blogs/', BlogPostListAPIView.as_view(), name='blog-list'),
    path('blogs/<int:pk>/', BlogPostDetailAPIView.as_view(), name='blog-detail'),
]