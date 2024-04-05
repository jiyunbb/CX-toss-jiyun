from apps.core import views as core_views
from django.urls import path

urlpatterns = [
    path("health/", core_views.HealthAPI.as_view()),
]
