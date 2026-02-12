from django.urls import include, path
from rest_framework.routers import DefaultRouter

from CarFleetManagement.emergency.views import EmergencyResponseCreateView

from .views import (
    AnalyzeScreenshotView,
    BatchAnalyzeScreenshotsView,
    DriverViewSet,
    EmergencyIncidentViewSet,
    GenerateReportView,
    MaintenanceViewSet,
    UserViewSet,
    VehicleViewSet,
)

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'vehicles', VehicleViewSet, basename='vehicle')
router.register(r'maintenance', MaintenanceViewSet, basename='maintenance')
router.register(r'emergencies', EmergencyIncidentViewSet, basename='emergencyincident')

router.register(r'drivers', DriverViewSet, basename='driver')

from .auth_views import LoginView, LogoutView, RegisterView, UserProfileView, ValidateTokenView

urlpatterns = [
    path('', include(router.urls)),
    path('auth/register/', RegisterView.as_view(), name='auth_register'),
    path('auth/login/', LoginView.as_view(), name='auth_login'),
    path('auth/logout/', LogoutView.as_view(), name='auth_logout'),
    path('auth/profile/', UserProfileView.as_view(), name='auth_profile'),
    path('auth/validate-token/', ValidateTokenView.as_view(), name='auth_validate_token'),
    path('analyze-screenshot/', AnalyzeScreenshotView.as_view(), name='analyze_screenshot'),
    path('batch-analyze-screenshots/', BatchAnalyzeScreenshotsView.as_view(), name='batch_analyze_screenshots'),
    path('generate-report/', GenerateReportView.as_view(), name='generate_report'),
    path('emergencies/<int:incident_id>/response/create/', EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
]
