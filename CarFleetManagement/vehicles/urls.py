from django.urls import path

from . import views

app_name = 'vehicles'

urlpatterns = [
    path('', views.VehicleListView.as_view(), name='vehicle_list'),
    path('<int:pk>/', views.VehicleDetailView.as_view(), name='vehicle_detail'),
    path('create/', views.VehicleCreateView.as_view(), name='vehicle_create'),
    path('<int:pk>/update/', views.VehicleUpdateView.as_view(), name='vehicle_update'),
    path('<int:pk>/delete/', views.VehicleDeleteView.as_view(), name='vehicle_delete'),
]
