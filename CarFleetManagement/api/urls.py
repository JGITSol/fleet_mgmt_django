"""URL patterns for the API app.

This module defines the URL patterns for the API endpoints,
including the screenshot analysis endpoints.
"""

from django.urls import path
from . import views

urlpatterns = [
    path('screenshots/analyze/', views.AnalyzeScreenshotView.as_view(), name='analyze_screenshot'),
    path('screenshots/batch-analyze/', views.BatchAnalyzeScreenshotsView.as_view(), name='batch_analyze_screenshots'),
    path('screenshots/generate-report/', views.GenerateReportView.as_view(), name='generate_report'),
]