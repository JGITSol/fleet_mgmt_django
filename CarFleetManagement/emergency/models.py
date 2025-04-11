from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import CustomUser
from vehicles.models import Vehicle

class EmergencyType(models.TextChoices):
    ACCIDENT = 'ACCIDENT', _('Accident')
    BREAKDOWN = 'BREAKDOWN', _('Breakdown')
    MEDICAL = 'MEDICAL', _('Medical Emergency')
    THEFT = 'THEFT', _('Theft')
    OTHER = 'OTHER', _('Other')

class EmergencyStatus(models.TextChoices):
    REPORTED = 'REPORTED', _('Reported')
    RESPONDING = 'RESPONDING', _('Responding')
    RESOLVED = 'RESOLVED', _('Resolved')
    CLOSED = 'CLOSED', _('Closed')

class EmergencyIncident(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='emergency_incidents')
    driver = models.ForeignKey('accounts.Driver', on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_incidents')
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_incidents')
    emergency_type = models.CharField(max_length=20, choices=EmergencyType.choices, default=EmergencyType.OTHER)
    status = models.CharField(max_length=20, choices=EmergencyStatus.choices, default=EmergencyStatus.REPORTED)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    description = models.TextField()
    reported_time = models.DateTimeField(auto_now_add=True)
    resolved_time = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.get_emergency_type_display()} - {self.vehicle} - {self.reported_time.strftime('%Y-%m-%d %H:%M')}"

class EmergencyResponse(models.Model):
    incident = models.ForeignKey(EmergencyIncident, on_delete=models.CASCADE, related_name='responses')
    responder = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emergency_responses')
    response_time = models.DateTimeField(auto_now_add=True)
    action_taken = models.TextField()
    notes = models.TextField(blank=True)
    
    def __str__(self):
        return f"Response to {self.incident} by {self.responder.username}"

class EmergencyContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emergency_contact_list')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.relationship} of {self.user.username})"
