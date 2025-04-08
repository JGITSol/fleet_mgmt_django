"""URL patterns for the API app.

This module defines the URL patterns for the API endpoints,
including the screenshot analysis endpoints and authentication endpoints for Lynx JS.
"""

from django.urls import path
from . import views
from . import auth_views
from rest_framework.authtoken.views import obtain_auth_token

# Authentication URLs for Lynx JS mobile app
auth_urlpatterns = [
    path('auth/register/', auth_views.RegisterView.as_view(), name='api_register'),
    path('auth/login/', auth_views.LoginView.as_view(), name='api_login'),
    path('auth/logout/', auth_views.LogoutView.as_view(), name='api_logout'),
    path('auth/profile/', auth_views.UserProfileView.as_view(), name='api_profile'),
    path('auth/validate-token/', auth_views.ValidateTokenView.as_view(), name='api_validate_token'),
    path('auth/token/', obtain_auth_token, name='api_token'),  # Default DRF token endpoint
]

# Screenshot analysis URLs
screenshot_urlpatterns = [
    path('screenshots/analyze/', views.AnalyzeScreenshotView.as_view(), name='analyze_screenshot'),
    path('screenshots/batch-analyze/', views.BatchAnalyzeScreenshotsView.as_view(), name='batch_analyze_screenshots'),
    path('screenshots/generate-report/', views.GenerateReportView.as_view(), name='generate_report'),
]

# Combine all URL patterns
urlpatterns = auth_urlpatterns + screenshot_urlpatterns