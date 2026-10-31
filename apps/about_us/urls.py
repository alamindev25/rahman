from django.urls import path
from .views import AboutUsAPIView

urlpatterns = [
    path('about-us/', AboutUsAPIView.as_view(), name='about_us'),
]