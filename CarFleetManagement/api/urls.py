"""URL patterns for the API app.

This module defines the URL patterns for the API endpoints,
including the screenshot analysis endpoints and authentication endpoints for Lynx JS.
"""

from django.urls import path

# drf-spectacular views for OpenAPI schema and UIs
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)
from rest_framework.response import Response
from rest_framework.views import APIView

from . import auth_views, views

app_name = "CarFleetManagement.api"


class ApiRootView(APIView):
    def get(self, request, *args, **kwargs):
        return Response({
            "message": "Welcome to the Car Fleet Management API.",
            "endpoints": [
                "/api/auth/",
                "/api/screenshots/",
                "/api/vehicles/",
                "/api/maintenance/",
                "/api/drivers/",
                "/api/emergencies/",
            ],
        })


# Authentication URLs for Lynx JS mobile app
auth_urlpatterns = [
    path("auth/register/", auth_views.RegisterView.as_view(), name="api_register"),
    path("auth/login/", auth_views.LoginView.as_view(), name="api_login"),
    path("auth/logout/", auth_views.LogoutView.as_view(), name="api_logout"),
    path("auth/profile/", auth_views.UserProfileView.as_view(), name="api_profile"),
    path("auth/validate-token/", auth_views.ValidateTokenView.as_view(), name="api_validate_token"),
    # Removed legacy token endpoint. Use JWT endpoints only.
]

# Screenshot analysis URLs
screenshot_urlpatterns = [
    path("screenshots/analyze/", views.AnalyzeScreenshotView.as_view(), name="analyze_screenshot"),
    path("screenshots/batch-analyze/", views.BatchAnalyzeScreenshotsView.as_view(), name="batch_analyze_screenshots"),
    path("screenshots/generate-report/", views.GenerateReportView.as_view(), name="generate_report"),
]

# Vehicle API URLs
vehicle_urlpatterns = [
    path("vehicles/", views.VehicleListCreateAPIView.as_view(), name="api-vehicle-list"),
    path("vehicles/<int:pk>/", views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name="api-vehicle-detail"),
]

# Maintenance API URLs
maintenance_urlpatterns = [
    path("maintenance/", views.MaintenanceListCreateAPIView.as_view(), name="maintenance_list"),
    path("maintenance/", views.MaintenanceListCreateAPIView.as_view(), name="api-maintenance-list"),
    path("maintenance/create/", views.MaintenanceListCreateAPIView.as_view(), name="maintenance_create"),
    path("maintenance/create/", views.MaintenanceListCreateAPIView.as_view(), name="api-maintenance-create"),
    path("maintenance/<int:pk>/", views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name="maintenance_detail"),
    path(
        "maintenance/<int:pk>/", views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name="api-maintenance-detail"
    ),
    path(
        "maintenance/<int:pk>/update/",
        views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(),
        name="maintenance_update",
    ),
    path(
        "maintenance/<int:pk>/update/",
        views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(),
        name="api-maintenance-update",
    ),
    path(
        "maintenance/<int:pk>/delete/",
        views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(),
        name="maintenance_delete",
    ),
    path(
        "maintenance/<int:pk>/delete/",
        views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(),
        name="api-maintenance-delete",
    ),
]

# Driver API URLs
driver_urlpatterns = [
    path("drivers/", views.DriverListCreateAPIView.as_view(), name="api-driver-list"),
    path("drivers/<int:pk>/", views.DriverRetrieveUpdateDestroyAPIView.as_view(), name="api-driver-detail"),
]

# Emergency API URLs
emergency_urlpatterns = [
    path("emergencies/", views.EmergencyIncidentListCreateAPIView.as_view(), name="api-emergency-list"),
    path(
        "emergencies/<int:pk>/",
        views.EmergencyIncidentRetrieveUpdateDestroyAPIView.as_view(),
        name="api-emergency-detail",
    ),
    path(
        "emergencies/responses/", views.EmergencyResponseListCreateAPIView.as_view(), name="api-emergency-response-list"
    ),
    path(
        "emergencies/responses/<int:pk>/",
        views.EmergencyResponseRetrieveUpdateDestroyAPIView.as_view(),
        name="api-emergency-response-detail",
    ),
]

# Vehicle Media API URLs
vehicle_media_urlpatterns = [
    path("vehicles/media/", views.VehicleMediaListCreateAPIView.as_view(), name="api-vehicle-media-list"),
    path("vehicles/media/<int:pk>/", views.VehicleMediaRetrieveUpdateDestroyAPIView.as_view(), name="api-vehicle-media-detail"),
]

# Combine all URL patterns
urlpatterns = [
    path("", ApiRootView.as_view(), name="api-root"),
    *auth_urlpatterns,
    *screenshot_urlpatterns,
    *vehicle_urlpatterns,
    *maintenance_urlpatterns,
    *driver_urlpatterns,
    *emergency_urlpatterns,
    *vehicle_media_urlpatterns,
]

# OpenAPI schema and documentation UIs (drf-spectacular)
# Exposed at /api/schema/ and /api/schema/swagger-ui/ and /api/schema/redoc/
schema_urlpatterns = [
    path("schema/", SpectacularAPIView.as_view(), name="schema"),
    # Use explicit schema URL to avoid reverse lookup issues when included under a namespace
    path("schema/swagger-ui/", SpectacularSwaggerView.as_view(url="/api/schema/"), name="swagger-ui"),
    path("schema/redoc/", SpectacularRedocView.as_view(url="/api/schema/"), name="redoc"),
]

urlpatterns += schema_urlpatterns
