from django.contrib import admin
from .models import EmergencyContact, EmergencyIncident, EmergencyResponse

@admin.register(EmergencyIncident)
class EmergencyIncidentAdmin(admin.ModelAdmin):
    list_display = ('emergency_type', 'vehicle', 'driver', 'status', 'reported_time')
    list_filter = ('emergency_type', 'status', 'reported_time')
    search_fields = ('vehicle__license_plate', 'driver__first_name', 'driver__last_name', 'location', 'description')
    readonly_fields = ('reported_time',)
    raw_id_fields = ('vehicle', 'driver', 'reported_by')

@admin.register(EmergencyResponse)
class EmergencyResponseAdmin(admin.ModelAdmin):
    list_display = ('incident', 'responder', 'response_time')
    list_filter = ('response_time',)
    search_fields = ('incident__description', 'responder__username', 'action_taken')
    readonly_fields = ('response_time',)
    raw_id_fields = ('incident', 'responder')

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'relationship', 'phone_number')
    list_filter = ('relationship',)
    search_fields = ('name', 'user__username', 'phone_number')
    raw_id_fields = ('user',)
