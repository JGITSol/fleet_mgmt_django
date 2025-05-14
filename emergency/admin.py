from django.contrib import admin
from .models import EmergencyIncident

@admin.register(EmergencyIncident)
class EmergencyIncidentAdmin(admin.ModelAdmin):
    list_display = ('incident_type', 'status', 'reported_time', 'resolved_time')
    search_fields = ('description', 'location')
    list_filter = ('incident_type', 'status')
