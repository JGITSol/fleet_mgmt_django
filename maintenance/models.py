from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from vehicles.models import Vehicle

class MaintenanceType(models.TextChoices):
    ROUTINE = 'ROUTINE', _('Routine Maintenance')
    REPAIR = 'REPAIR', _('Repair')
    INSPECTION = 'INSPECTION', _('Inspection')
    OTHER = 'OTHER', _('Other')

class MaintenanceStatus(models.TextChoices):
    SCHEDULED = 'SCHEDULED', _('Scheduled')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Maintenance(models.Model):
    vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE, related_name='maintenance_records', verbose_name=_('Vehicle'))
    maintenance_type = models.CharField(max_length=15, choices=MaintenanceType.choices, default=MaintenanceType.ROUTINE, verbose_name=_('Maintenance Type'))
    status = models.CharField(max_length=15, choices=MaintenanceStatus.choices, default=MaintenanceStatus.SCHEDULED, verbose_name=_('Maintenance Status'))
    description = models.TextField(verbose_name=_('Maintenance Description'))
    odometer_reading = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name=_('Odometer Reading'), null=True, blank=True)
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Cost'))
    service_provider = models.CharField(max_length=100, blank=True, verbose_name=_('Service Provider'))
    scheduled_date = models.DateField(verbose_name=_('Scheduled Date'))
    completed_date = models.DateField(null=True, blank=True, verbose_name=_('Completed Date'))
    notes = models.TextField(blank=True, verbose_name=_('Notes'))

    def days_until_scheduled(self):
        from django.utils import timezone
        if not self.scheduled_date:
            return 0
        today = timezone.now().date()
        delta = (self.scheduled_date - today).days
        return delta

    def __str__(self):
        # Example: 'Toyota Camry (ABC-123) - Oil Change - 2025-04-17'
        vehicle_str = str(self.vehicle) if self.vehicle else 'Unknown Vehicle'
        type_str = self.maintenance_type.title() if self.maintenance_type else 'Unknown Type'
        date_str = self.scheduled_date.strftime('%Y-%m-%d') if self.scheduled_date else 'No Date'
        return f"{vehicle_str} - {type_str} - {date_str}"
