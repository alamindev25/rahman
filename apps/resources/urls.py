from django.urls import path
from .views import ResourceItemListView, ResourceItemDetailView

urlpatterns = [
    path("resources/", ResourceItemListView.as_view(), name="resource-list"),
    path("resources/<int:pk>/", ResourceItemDetailView.as_view(), name="resource-detail"),
]
