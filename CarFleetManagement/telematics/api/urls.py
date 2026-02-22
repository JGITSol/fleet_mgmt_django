from django.urls import path
from . import views

app_name = "telematics"

urlpatterns = [
    path('gps/', views.GPSLocationListCreateAPIView.as_view(), name='gps-list'),
    path('trips/', views.TripListCreateAPIView.as_view(), name='trip-list'),
    path('fuel/', views.FuelLogListCreateAPIView.as_view(), name='fuel-list'),
    path('driver-scores/', views.DriverScoreListCreateAPIView.as_view(), name='driver-score-list'),
    path('alerts/', views.AlertListCreateAPIView.as_view(), name='alert-list'),
    path('inspections/', views.InspectionListCreateAPIView.as_view(), name='inspection-list'),
]
