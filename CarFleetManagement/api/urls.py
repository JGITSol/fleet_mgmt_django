"""URL patterns for the API app.

This module defines the URL patterns for the API endpoints,
including the screenshot analysis endpoints and authentication endpoints for Lynx JS.
"""

app_name = "CarFleetManagement.api"
from django.urls import path
from . import views
from . import auth_views

# Authentication URLs for Lynx JS mobile app
auth_urlpatterns = [
    path('auth/register/', auth_views.RegisterView.as_view(), name='api_register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='api_login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='api_logout'),
    path('auth/profile/', auth_views.UserProfileView.as_view(), name='api_profile'),
    path('auth/validate-token/', auth_views.ValidateTokenView.as_view(), name='api_validate_token'),
    # Removed legacy token endpoint. Use JWT endpoints only.
]

# Screenshot analysis URLs
screenshot_urlpatterns = [
    path('screenshots/analyze/', views.AnalyzeScreenshotView.as_view(), name='analyze_screenshot'),
    path('screenshots/batch-analyze/', views.BatchAnalyzeScreenshotsView.as_view(), name='batch_analyze_screenshots'),
    path('screenshots/generate-report/', views.GenerateReportView.as_view(), name='generate_report'),
]

# Vehicle API URLs
vehicle_urlpatterns = [
    path('vehicles/', views.VehicleListCreateAPIView.as_view(), name='vehicle_list'),
    path('vehicles/', views.VehicleListCreateAPIView.as_view(), name='api-vehicle-list'),
    path('vehicles/create/', views.VehicleListCreateAPIView.as_view(), name='vehicle_create'),
    path('vehicles/create/', views.VehicleListCreateAPIView.as_view(), name='api-vehicle-create'),
    path('vehicles/<int:pk>/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle_detail'),
    path('vehicles/<int:pk>/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='api-vehicle-detail'),
    path('vehicles/<int:pk>/update/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle_update'),
    path('vehicles/<int:pk>/update/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='api-vehicle-update'),
    path('vehicles/<int:pk>/delete/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='vehicle_delete'),
    path('vehicles/<int:pk>/delete/', views.VehicleRetrieveUpdateDestroyAPIView.as_view(), name='api-vehicle-delete'),
]

# Maintenance API URLs
maintenance_urlpatterns = [
    path('maintenance/', views.MaintenanceListCreateAPIView.as_view(), name='maintenance_list'),
    path('maintenance/', views.MaintenanceListCreateAPIView.as_view(), name='api-maintenance-list'),
    path('maintenance/create/', views.MaintenanceListCreateAPIView.as_view(), name='maintenance_create'),
    path('maintenance/create/', views.MaintenanceListCreateAPIView.as_view(), name='api-maintenance-create'),
    path('maintenance/<int:pk>/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='maintenance_detail'),
    path('maintenance/<int:pk>/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='api-maintenance-detail'),
    path('maintenance/<int:pk>/update/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='maintenance_update'),
    path('maintenance/<int:pk>/update/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='api-maintenance-update'),
    path('maintenance/<int:pk>/delete/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='maintenance_delete'),
    path('maintenance/<int:pk>/delete/', views.MaintenanceRetrieveUpdateDestroyAPIView.as_view(), name='api-maintenance-delete'),
]

# Driver API URLs
driver_urlpatterns = [
    path('drivers/', views.DriverListCreateAPIView.as_view(), name='api-driver-list'),
    path('drivers/<int:pk>/', views.DriverRetrieveUpdateDestroyAPIView.as_view(), name='api-driver-detail'),
]

# Emergency API URLs
emergency_urlpatterns = [
    path('emergencies/', views.EmergencyIncidentListCreateAPIView.as_view(), name='emergency_list'),
    path('emergencies/', views.EmergencyIncidentListCreateAPIView.as_view(), name='api-emergency-list'),
    path('emergencies/create/', views.EmergencyIncidentListCreateAPIView.as_view(), name='emergency_create'),
    path('emergencies/create/', views.EmergencyIncidentListCreateAPIView.as_view(), name='api-emergency-create'),
    path('emergencies/<int:pk>/', views.EmergencyIncidentRetrieveUpdateDestroyAPIView.as_view(), name='emergency_detail'),
    path('emergencies/<int:pk>/', views.EmergencyIncidentRetrieveUpdateDestroyAPIView.as_view(), name='api-emergency-detail'),
    path('emergencies/<int:pk>/update/', views.EmergencyIncidentUpdateAPIView.as_view(), name='emergency_update'),
    path('emergencies/<int:pk>/update/', views.EmergencyIncidentUpdateAPIView.as_view(), name='api-emergency-update'),
    path('emergencies/<int:pk>/delete/', views.EmergencyIncidentDeleteAPIView.as_view(), name='emergency_delete'),
    path('emergencies/<int:pk>/delete/', views.EmergencyIncidentDeleteAPIView.as_view(), name='api-emergency-delete'),
    path('emergencies/<int:incident_id>/response/create/', views.EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
    path('emergencies/<int:incident_id>/response/create/', views.EmergencyResponseCreateView.as_view(), name='api-emergency-response-create'),
]

# Combine all URL patterns
urlpatterns = auth_urlpatterns + screenshot_urlpatterns + vehicle_urlpatterns + maintenance_urlpatterns + driver_urlpatterns + emergency_urlpatterns