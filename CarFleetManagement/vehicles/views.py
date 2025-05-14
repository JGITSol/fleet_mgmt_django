from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Vehicle
from .serializers import VehicleSerializer

# Vehicle Views
class VehicleListView(LoginRequiredMixin, ListView):
    model = Vehicle
    template_name = 'vehicles/vehicle_list.html'
    context_object_name = 'vehicles'
    
    def get_queryset(self):
        return Vehicle.objects.all().order_by('-created_at')

class VehicleDetailView(LoginRequiredMixin, DetailView):
    model = Vehicle
    template_name = 'vehicles/vehicle_detail.html'
    context_object_name = 'vehicle'

class VehicleCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields = ['brand', 'model', 'year', 'license_plate', 'vin', 'color', 'fuel_type', 
              'transmission', 'vehicle_type', 'mileage', 'last_service_date', 
              'next_service_date', 'insurance_expiry', 'status']
    success_url = reverse_lazy('vehicle_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Vehicle created successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Only fleet managers and admins can create vehicles
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'FLEET_MANAGER']

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields = ['brand', 'model', 'year', 'license_plate', 'vin', 'color', 'fuel_type', 
              'transmission', 'vehicle_type', 'mileage', 'last_service_date', 
              'next_service_date', 'insurance_expiry', 'status']
    
    def get_success_url(self):
        return reverse_lazy('vehicle_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Only fleet managers and admins can update vehicles
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'FLEET_MANAGER']

class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicle_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vehicle deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        # Only fleet managers and admins can delete vehicles
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'FLEET_MANAGER']
