from django.db import models
from django.utils.translation import gettext_lazy as _

from CarFleetManagement.accounts.models import CustomUser, Driver
from CarFleetManagement.vehicles.models import Vehicle


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
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='emergency_incidents', verbose_name=_('Vehicle'))
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_incidents', verbose_name=_('Driver'))
    reported_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='reported_incidents', verbose_name=_('Reported By'))
    emergency_type = models.CharField(max_length=20, choices=EmergencyType.choices, default=EmergencyType.OTHER, verbose_name=_('Emergency Type'))
    status = models.CharField(max_length=20, choices=EmergencyStatus.choices, default=EmergencyStatus.REPORTED, verbose_name=_('Status'))
    location = models.CharField(max_length=255, blank=True, verbose_name=_('Location'))
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True, verbose_name=_('Longitude'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    reported_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Reported Time'))
    resolved_time = models.DateTimeField(null=True, blank=True, verbose_name=_('Resolved Time'))
    attachment = models.ImageField(upload_to='emergency/incidents/', null=True, blank=True, verbose_name=_('Attachment'))
    video_attachment = models.FileField(upload_to='emergency/videos/', null=True, blank=True, verbose_name=_('Video Attachment'))

    def __str__(self):
        return f"{self.get_emergency_type_display()} - {self.vehicle} - {self.reported_time.strftime('%Y-%m-%d %H:%M')}"

class EmergencyResponse(models.Model):
    incident = models.ForeignKey(EmergencyIncident, on_delete=models.CASCADE, related_name='responses', verbose_name=_('Incident'))
    responder = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank=True, related_name='emergency_responses', verbose_name=_('Responder'))
    response_time = models.DateTimeField(auto_now_add=True, verbose_name=_('Response Time'))
    action_taken = models.TextField(null=True, blank=True, verbose_name=_('Action Taken'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))
    attachment = models.FileField(upload_to='emergency/responses/', null=True, blank=True, verbose_name=_('Response Attachment'))

    def __str__(self):
        return f"Response to {self.incident} by {self.responder.username}"

class EmergencyContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emergency_contact_list', verbose_name=_('User'))
    name = models.CharField(max_length=100, verbose_name=_('Name'))
    phone_number = models.CharField(max_length=15, verbose_name=_('Phone Number'))
    relationship = models.CharField(max_length=50, verbose_name=_('Relationship'))

    def __str__(self):
        return f"{self.name} ({self.relationship}) - {self.phone_number}"
