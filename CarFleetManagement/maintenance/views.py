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
from CarFleetManagement.vehicles.models import Vehicle

from .models import Maintenance


# Maintenance Views
class MaintenanceListView(LoginRequiredMixin, ListView):
    model = Maintenance
    template_name = 'maintenance/maintenance_list.html'
    # tests and templates expect the context variable name 'maintenance_list'
    # (Django's ListView default is '<model>_list'). Keep that name so
    # test-created objects appear in the template loop.
    context_object_name = 'maintenance_list'

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
    success_url = reverse_lazy('maintenance:maintenance_list')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Only show available vehicles in the dropdown
        form.fields['vehicle'].queryset = Vehicle.objects.filter(status='AVAILABLE')
        return form

    def form_valid(self, form):
        messages.success(self.request, 'Maintenance record created successfully!')
        return super().form_valid(form)

    def test_func(self):
        # Only maintenance staff and admins can create maintenance records.
        # Use the project's UserRole constants (which store lowercase names).
        if self.request.user.is_staff:
            return True
        if hasattr(self.request.user, 'role') and self.request.user.role is not None:
            return self.request.user.role.name in [UserRole.ADMIN, UserRole.MAINTENANCE_STAFF]
        return False

class MaintenanceUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Maintenance
    template_name = 'maintenance/maintenance_form.html'
    fields = ['vehicle', 'maintenance_type', 'status', 'description', 'scheduled_date',
              'completed_date', 'odometer_reading', 'cost', 'service_provider', 'notes']

    def get_success_url(self):
        return reverse_lazy('maintenance:maintenance_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        messages.success(self.request, 'Maintenance record updated successfully!')
        return super().form_valid(form)

    def test_func(self):
        # Only maintenance staff and admins can update maintenance records.
        if self.request.user.is_staff:
            return True
        if hasattr(self.request.user, 'role') and self.request.user.role is not None:
            return self.request.user.role.name in [UserRole.ADMIN, UserRole.MAINTENANCE_STAFF]
        return False

class MaintenanceDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Maintenance
    template_name = 'maintenance/maintenance_confirm_delete.html'
    success_url = reverse_lazy('maintenance:maintenance_list')

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Maintenance record deleted successfully!')
        return super().delete(request, *args, **kwargs)

    def test_func(self):
        # Only maintenance staff and admins can delete maintenance records.
        if self.request.user.is_staff:
            return True
        if hasattr(self.request.user, 'role') and self.request.user.role is not None:
            return self.request.user.role.name in [UserRole.ADMIN, UserRole.MAINTENANCE_STAFF]
        return False
