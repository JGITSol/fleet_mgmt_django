from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.EmergencyIncidentListView.as_view(), name='emergency_list'),
    path('incident/<int:pk>/', views.EmergencyIncidentDetailView.as_view(), name='emergency_detail'),
    path('incident/new/', views.EmergencyIncidentCreateView.as_view(), name='emergency_create'),
    path('incident/<int:pk>/update/', views.EmergencyIncidentUpdateView.as_view(), name='emergency_update'),
    path('incident/<int:pk>/delete/', views.EmergencyIncidentDeleteView.as_view(), name='emergency_delete'),
    path('incident/<int:incident_id>/response/new/', views.EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
]
