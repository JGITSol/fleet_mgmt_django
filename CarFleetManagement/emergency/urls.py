from django.urls import path
from . import views

app_name = 'emergency'

urlpatterns = [
    path('', views.EmergencyIncidentListView.as_view(), name='emergency_list'),
    path('<int:pk>/', views.EmergencyIncidentDetailView.as_view(), name='emergency_detail'),
    path('create/', views.EmergencyIncidentCreateView.as_view(), name='emergency_create'),
    path('<int:pk>/update/', views.EmergencyIncidentUpdateView.as_view(), name='emergency_update'),
    path('<int:pk>/delete/', views.EmergencyIncidentDeleteView.as_view(), name='emergency_delete'),
    path('<int:incident_id>/response/create/', views.EmergencyResponseCreateView.as_view(), name='emergency_response_create'),
]
