from typing import ClassVar

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    DetailView,
    ListView,
    UpdateView,
)

from CarFleetManagement.accounts.models import UserRole

from .models import Vehicle


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
    fields: ClassVar[list[str]] = ['brand', 'model', 'year', 'license_plate', 'vin', 'color', 'fuel_type',
              'transmission', 'vehicle_type', 'mileage', 'last_service_date',
              'next_service_date', 'insurance_expiry', 'status']
    success_url = reverse_lazy('vehicles:vehicle_list')

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle created successfully!')
        return super().form_valid(form)

    def test_func(self):
        # Only fleet managers (manager role) and admins can create vehicles
        if not (self.request.user and getattr(self.request.user, 'is_authenticated', False)):
            return False
        if getattr(self.request.user, 'is_staff', False) or getattr(self.request.user, 'is_superuser', False):
            return True
        return hasattr(self.request.user, 'role') and self.request.user.role.name in [UserRole.ADMIN, UserRole.MANAGER]

class VehicleUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Vehicle
    template_name = 'vehicles/vehicle_form.html'
    fields: ClassVar[list[str]] = ['brand', 'model', 'year', 'license_plate', 'vin', 'color', 'fuel_type',
              'transmission', 'vehicle_type', 'mileage', 'last_service_date',
              'next_service_date', 'insurance_expiry', 'status']

    def get_success_url(self):
        return reverse_lazy('vehicles:vehicle_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Vehicle updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        # Only fleet managers (manager role) and admins can update vehicles
        if not (self.request.user and getattr(self.request.user, 'is_authenticated', False)):
            return False
        if getattr(self.request.user, 'is_staff', False) or getattr(self.request.user, 'is_superuser', False):
            return True
        return hasattr(self.request.user, 'role') and self.request.user.role.name in [UserRole.ADMIN, UserRole.MANAGER]

class VehicleDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Vehicle
    template_name = 'vehicles/vehicle_confirm_delete.html'
    success_url = reverse_lazy('vehicles:vehicle_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Vehicle deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # Only fleet managers (manager role) and admins can delete vehicles
        if not (self.request.user and getattr(self.request.user, 'is_authenticated', False)):
            return False
        if getattr(self.request.user, 'is_staff', False) or getattr(self.request.user, 'is_superuser', False):
            return True
        return hasattr(self.request.user, 'role') and self.request.user.role.name in [UserRole.ADMIN, UserRole.MANAGER]
