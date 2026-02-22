from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MinValueValidator, MaxValueValidator

from CarFleetManagement.vehicles.models import Vehicle
from CarFleetManagement.accounts.models import Driver

class GPSLocation(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='gps_locations')
    latitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Latitude'))
    longitude = models.DecimalField(max_digits=9, decimal_places=6, verbose_name=_('Longitude'))
    speed = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_('Speed (km/h)'))
    heading = models.DecimalField(max_digits=5, decimal_places=2, default=0, verbose_name=_('Heading (degrees)'))
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_('Timestamp'))

    class Meta:
        ordering = ['-timestamp']
        verbose_name = _('GPS Location')
        verbose_name_plural = _('GPS Locations')

    def __str__(self):
        return f"{self.vehicle} @ {self.timestamp}"

class Trip(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='trips')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True, related_name='trips')
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(null=True, blank=True, verbose_name=_('End Time'))
    start_location = models.CharField(max_length=255, verbose_name=_('Start Location'))
    end_location = models.CharField(max_length=255, blank=True, verbose_name=_('End Location'))
    distance_km = models.DecimalField(max_digits=8, decimal_places=2, default=0, verbose_name=_('Distance (km)'))

    class Meta:
        ordering = ['-start_time']
        verbose_name = _('Trip')
        verbose_name_plural = _('Trips')

class FuelLog(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='fuel_logs')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True, blank=True)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_('Date'))
    liters = models.DecimalField(max_digits=6, decimal_places=2, verbose_name=_('Liters Filled'))
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('Total Cost'))
    odometer = models.PositiveIntegerField(verbose_name=_('Odometer Reading'))
    receipt_image = models.ImageField(upload_to='telematics/fuel_receipts/', null=True, blank=True)

    class Meta:
        ordering = ['-date']

class DriverScore(models.Model):
    driver = models.OneToOneField(Driver, on_delete=models.CASCADE, related_name='score_profile')
    safety_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    eco_score = models.IntegerField(validators=[MinValueValidator(0), MaxValueValidator(100)], default=100)
    total_harsh_brakes = models.PositiveIntegerField(default=0)
    total_speeding_events = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Score: {self.driver} - Safety: {self.safety_score}"

class Alert(models.Model):
    class AlertType(models.TextChoices):
        SPEEDING = 'SPEEDING', _('Speeding')
        GEOFENCE = 'GEOFENCE', _('Geofence Violation')
        MAINTENANCE = 'MAINTENANCE', _('Maintenance Overdue')
        IDLING = 'IDLING', _('Excessive Idling')

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='alerts')
    alert_type = models.CharField(max_length=20, choices=AlertType.choices)
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

class Inspection(models.Model):
    class ResultChoices(models.TextChoices):
        PASS = 'PASS', _('Pass')
        FAIL = 'FAIL', _('Fail')

    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='inspections')
    driver = models.ForeignKey(Driver, on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    is_pre_trip = models.BooleanField(default=True, verbose_name=_('Is Pre-Trip?'))
    result = models.CharField(max_length=10, choices=ResultChoices.choices)
    notes = models.TextField(blank=True)

    class Meta:
        ordering = ['-date']
