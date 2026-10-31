from django.urls import path
from .views import LanguageListAPIView, DefaultLanguageAPIView

urlpatterns = [
    path('languages/', LanguageListAPIView.as_view(), name='language-list'),
    path('languages/default/', DefaultLanguageAPIView.as_view(), name='language-default'),
]
