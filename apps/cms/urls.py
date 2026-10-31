from django.urls import path
from .views import CMSPageView,FAQListView

urlpatterns = [
    path("cms/", CMSPageView.as_view(), name="cms_data"),
    path('faqs/', FAQListView.as_view()),
]