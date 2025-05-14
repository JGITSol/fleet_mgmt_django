from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages

from .models import Maintenance
from vehicles.models import Vehicle
from .serializers import MaintenanceSerializer

# Maintenance Views
class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenance/maintenance_list.html'
    context_object_name = 'maintenance_records'
    
    def get_queryset(self):
        return Maintenance.objects.all().order_by('-scheduled_date')

class MaintenanceDetailView(LoginRequiredMixin, DetailView):
    model = Maintenance
    template_name = 'maintenance/maintenance_detail.html'
    context_object_name = 'maintenance'

class MaintenanceCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Maintenance
    template_name = 'maintenance/maintenance_form.html'
    fields = ['vehicle', 'maintenance_type', 'status', 'description', 'scheduled_date',
              'completed_date', 'odometer_reading', 'cost', 'service_provider', 'notes']
    success_url = reverse_lazy('maintenance_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show available vehicles in the dropdown
        form.fields['vehicle'].queryset = Vehicle.objects.filter(status='AVAILABLE')
        return form
    
    def form_valid(self, form):
        messages.success(self.request, 'Maintenance record created successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Only maintenance staff and admins can create maintenance records
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'MAINTENANCE_STAFF']

class MaintenanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Maintenance
    template_name = 'maintenance/maintenance_form.html'
    fields = ['vehicle', 'maintenance_type', 'status', 'description', 'scheduled_date',
              'completed_date', 'odometer_reading', 'cost', 'service_provider', 'notes']
    
    def get_success_url(self):
        return reverse_lazy('maintenance_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        messages.success(self.request, 'Maintenance record updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Only maintenance staff and admins can update maintenance records
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'MAINTENANCE_STAFF']

class MaintenanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Maintenance record deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        # Only maintenance staff and admins can delete maintenance records
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'MAINTENANCE_STAFF']
