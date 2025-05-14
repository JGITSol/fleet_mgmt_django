from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from accounts.models import Driver  # fix for direct reference

class IncidentType(models.TextChoices):
    ACCIDENT = 'ACCIDENT', _('Accident')
    BREAKDOWN = 'BREAKDOWN', _('Breakdown')
    MEDICAL = 'MEDICAL', _('Medical')
    THEFT = 'THEFT', _('Theft')

class IncidentStatus(models.TextChoices):
    REPORTED = 'REPORTED', _('Reported')
    RESPONDING = 'RESPONDING', _('Responding')
    RESOLVED = 'RESOLVED', _('Resolved')
    CLOSED = 'CLOSED', _('Closed')

# Aliases for compatibility with tests
EmergencyType = IncidentType
EmergencyStatus = IncidentStatus

class EmergencyIncident(models.Model):
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices, verbose_name=_('Incident Type'))
    emergency_type = models.CharField(max_length=20, choices=IncidentType.choices, verbose_name=_('Emergency Type'), blank=True)
    status = models.CharField(max_length=20, choices=IncidentStatus.choices, default=IncidentStatus.REPORTED, verbose_name=_('Status'))
    description = models.TextField(verbose_name=_('Description'))
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_incidents')
    vehicle = models.ForeignKey('vehicles.Vehicle', on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_incidents')
    reported_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True, related_name='reported_emergencies')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    reported_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Reported Time'), null=True)
    resolved_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Resolved Time'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))

    def __str__(self):
        # Match test expectation: f"Accident - Toyota Camry (ABC-123) - {self.incident.reported_time.strftime('%Y-%m-%d %H:%M')}"
        veh = f"{self.vehicle.brand} {self.vehicle.model} ({self.vehicle.license_plate})" if self.vehicle else "Unknown Vehicle"
        t = self.emergency_type or self.incident_type
        return f"{t.title()} - {veh} - {self.reported_time.strftime('%Y-%m-%d %H:%M') if self.reported_time else ''}"

class EmergencyContact(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    relationship = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.phone_number}"

class EmergencyResponse(models.Model):
    incident = models.ForeignKey(EmergencyIncident, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    emergency_type = models.CharField(max_length=20, choices=IncidentType.choices)
    response_time = models.DateTimeField(auto_now_add=True)
    action_taken = models.TextField(null=True, blank=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        responder_str = str(self.responder) if self.responder else 'Unknown'
        return f"Response to {self.incident} by {responder_str}"
