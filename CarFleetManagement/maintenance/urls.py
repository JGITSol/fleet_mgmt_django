from django.urls import path
from . import views

app_name = 'maintenance'

urlpatterns = [
    path('', views.MaintenanceListView.as_view(), name='maintenance_list'),
    path('<int:pk>/', views.MaintenanceDetailView.as_view(), name='maintenance_detail'),
    path('create/', views.MaintenanceCreateView.as_view(), name='maintenance_create'),
    path('<int:pk>/update/', views.MaintenanceUpdateView.as_view(), name='maintenance_update'),
    path('<int:pk>/delete/', views.MaintenanceDeleteView.as_view(), name='maintenance_delete'),
]
