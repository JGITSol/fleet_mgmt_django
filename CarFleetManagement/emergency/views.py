from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib import messages
from django.shortcuts import get_object_or_404

from .models import EmergencyIncident, EmergencyResponse
from CarFleetManagement.vehicles.models import Vehicle

# Emergency Incident Views
class EmergencyIncidentListView(LoginRequiredMixin, ListView):
    model = EmergencyIncident
    template_name = 'emergency/emergency_list.html'
    context_object_name = 'incidents'
    
    def get_queryset(self):
        return EmergencyIncident.objects.all().order_by('-reported_time')

class EmergencyIncidentDetailView(LoginRequiredMixin, DetailView):
    model = EmergencyIncident
    template_name = 'emergency/emergency_detail.html'
    context_object_name = 'incident'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['responses'] = EmergencyResponse.objects.filter(incident=self.object).order_by('response_time')
        return context

class EmergencyIncidentCreateView(LoginRequiredMixin, CreateView):
    model = EmergencyIncident
    template_name = 'emergency/emergency_form.html'
    fields = ['vehicle', 'emergency_type', 'location', 'description', 'status', 'reported_by']
    success_url = reverse_lazy('emergency_list')
    
    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        # Show all vehicles in the dropdown
        form.fields['vehicle'].queryset = Vehicle.objects.all()
        return form
    
    def form_valid(self, form):
        form.instance.reported_by = self.request.user
        form.save()
        messages.success(self.request, 'Emergency incident reported successfully!')
        return super().form_valid(form)

class EmergencyIncidentUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = EmergencyIncident
    template_name = 'emergency/emergency_form.html'
    fields = ['vehicle', 'emergency_type', 'location', 'description', 'status', 'reported_by']
    
    def get_success_url(self):
        return reverse_lazy('emergency_detail', kwargs={'pk': self.object.pk})
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Emergency incident updated successfully!')
        return super().form_valid(form)
    
    def test_func(self):
        # Only admins and emergency staff can update incidents
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'EMERGENCY_STAFF']

class EmergencyIncidentDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = EmergencyIncident
    template_name = 'emergency/emergency_confirm_delete.html'
    success_url = reverse_lazy('emergency_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Emergency incident deleted successfully!')
        return super().delete(request, *args, **kwargs)
    
    def test_func(self):
        # Only admins can delete incidents
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name == 'ADMIN'

# Emergency Response Views
class EmergencyResponseCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = EmergencyResponse
    template_name = 'emergency/emergency_response_form.html'
    fields = ['responder', 'action_taken', 'notes']  # Removed response_time as it's auto-populated
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['incident'] = get_object_or_404(EmergencyIncident, id=self.kwargs['incident_id'])
        return context
    
    def form_valid(self, form):
        form.instance.incident = get_object_or_404(EmergencyIncident, id=self.kwargs['incident_id'])
        form.instance.responder = self.request.user
        form.save()
        messages.success(self.request, 'Emergency response recorded successfully!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('emergency_detail', kwargs={'pk': self.kwargs['incident_id']})
    
    def test_func(self):
        # Only emergency staff and admins can create responses
        return self.request.user.is_staff or hasattr(self.request.user, 'role') and self.request.user.role.name in ['ADMIN', 'EMERGENCY_STAFF']
