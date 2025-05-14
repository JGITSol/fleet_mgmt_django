from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    UserViewSet, VehicleViewSet, MaintenanceViewSet, EmergencyIncidentViewSet, DriverViewSet,
    AnalyzeScreenshotView, BatchAnalyzeScreenshotsView, GenerateReportView
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'emergencies', EmergencyIncidentViewSet, basename='emergencyincident')

# Add emergency response endpoints if not already present
from CarFleetManagement.emergency.views import EmergencyResponseCreateView
from django.urls import path

urlpatterns += [
    path('emergencies/<int:incident_id>/response/create/', EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
]

router.register(r'drivers', DriverViewSet, basename='driver')

urlpatterns = [
    path('', include(router.urls)),
    path('analyze-screenshot/', AnalyzeScreenshotView.as_view(), name='analyze_screenshot'),
    path('batch-analyze-screenshots/', BatchAnalyzeScreenshotsView.as_view(), name='batch_analyze_screenshots'),
    path('generate-report/', GenerateReportView.as_view(), name='generate_report'),
]
