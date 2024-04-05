from django.urls import path, include

from apps.certificates import views as certificates_views
from apps.core import views as core_views

urlpatterns = [
    path("health/", core_views.HealthAPI.as_view()),
    path("v1/", include([
        path("api/certificates/", certificates_views.CertificateListCreateView.as_view()),
        path("api/certificates/<int:certificate_id>/", certificates_views.CertificateHTML.as_view())
    ])),
]
