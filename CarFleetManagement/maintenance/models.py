from django.db import models
from django.core.validators import MinValueValidator
from django.utils.translation import gettext_lazy as _
from vehicles.models import Vehicle

class MaintenanceType(models.TextChoices):
    """Enumeration for maintenance types."""
    ROUTINE = 'ROUTINE', _('Routine Maintenance')
    REPAIR = 'REPAIR', _('Repair')
    INSPECTION = 'INSPECTION', _('Inspection')
    OTHER = 'OTHER', _('Other')

class MaintenanceStatus(models.TextChoices):
    """Enumeration for maintenance status values."""
    SCHEDULED = 'SCHEDULED', _('Scheduled')
    IN_PROGRESS = 'IN_PROGRESS', _('In Progress')
    COMPLETED = 'COMPLETED', _('Completed')
    CANCELLED = 'CANCELLED', _('Cancelled')

class Maintenance(models.Model):
    """
    Represents a maintenance record for a vehicle.

    Attributes:
        vehicle (Vehicle): The vehicle associated with this maintenance record.
        maintenance_type (str): Type of maintenance (routine, repair, inspection, etc).
        status (str): Current status of the maintenance (scheduled, in progress, completed, cancelled).
        description (str): Description of the maintenance work to be performed.
        scheduled_date (date): Date the maintenance is scheduled for.
        completed_date (date): Date the maintenance was completed.
        odometer_reading (int): Odometer reading at the time of maintenance.
        cost (Decimal): Cost of the maintenance.
        service_provider (str): Provider performing the maintenance.
        notes (str): Additional notes about the maintenance.
    """
    vehicle = models.ForeignKey(
        Vehicle, on_delete=models.CASCADE, related_name='maintenance_records',
        verbose_name=_('Vehicle'), help_text="Vehicle associated with this maintenance record."
    )
    maintenance_type = models.CharField(
        max_length=15, choices=MaintenanceType.choices, default=MaintenanceType.ROUTINE,
        verbose_name=_('Maintenance Type'), help_text="Type of maintenance (routine, repair, inspection, etc)."
    )
    status = models.CharField(
        max_length=15, choices=MaintenanceStatus.choices, default=MaintenanceStatus.SCHEDULED,
        verbose_name=_('Maintenance Status'), help_text="Current status of the maintenance."
    )
    description = models.TextField(
        verbose_name=_('Maintenance Description'), help_text="Description of the maintenance work to be performed."
    )
    scheduled_date = models.DateField(
        verbose_name=_('Scheduled Date'), help_text="Date the maintenance is scheduled for."
    )
    completed_date = models.DateField(
        null=True, blank=True, verbose_name=_('Completed Date'), help_text="Date the maintenance was completed."
    )
    odometer_reading = models.PositiveIntegerField(
        validators=[MinValueValidator(0)], verbose_name=_('Odometer Reading'), help_text="Odometer reading at the time of maintenance."
    )
    cost = models.DecimalField(
        max_digits=10, decimal_places=2, validators=[MinValueValidator(0)],
        verbose_name=_('Maintenance Cost'), help_text="Cost of the maintenance."
    )
    service_provider = models.CharField(
        max_length=100, verbose_name=_('Service Provider'), help_text="Provider performing the maintenance."
    )
    notes = models.TextField(
        blank=True, verbose_name=_('Additional Notes'), help_text="Additional notes about the maintenance."
    )
    
    def __str__(self):
        """Return a string representation of the maintenance record."""
        return f"{self.get_maintenance_type_display()} for {self.vehicle} on {self.scheduled_date}"
    
    def days_until_scheduled(self):
        """
        Calculate the number of days until the scheduled maintenance date.
        Returns 0 if scheduled for today, None if completed/cancelled or if scheduled date is in the past.
        Returns:
            int or None: Days until scheduled date, or None if not applicable.
        """
        from django.utils import timezone
        # Return None for completed or cancelled maintenance
        if self.status in [MaintenanceStatus.COMPLETED, MaintenanceStatus.CANCELLED]:
            return None
        
        # Handle case where scheduled_date is None
        if not self.scheduled_date:
            return 0 # Consistent with existing test_missing_scheduled_date
        
        today = timezone.now().date()
        
        # If scheduled date is in the past (and not completed/cancelled), return None
        if self.scheduled_date < today:
            return None
        
        # Calculate days difference using timezone-aware date
        delta = self.scheduled_date - today
        return delta.days
