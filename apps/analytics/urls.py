from django.urls import path
from .views.dashboard import AnalyticsDashboardView

app_name = "analytics"

urlpatterns = [
    path("dashboard/", AnalyticsDashboardView.as_view(), name="analytics-dashboard"),
]

