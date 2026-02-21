from django.db import models
from django.utils.translation import gettext_lazy as _


class Vehicle(models.Model):
    class VehicleType(models.TextChoices):
        TRUCK = 'TRUCK', _('Truck')
        VAN = 'VAN', _('Van')
        SUV = 'SUV', _('SUV')
        PICKUP = 'PICKUP', _('Pickup')

    class FuelType(models.TextChoices):
        DIESEL = 'DIESEL', _('Diesel')
        PETROL = 'PETROL', _('Petrol')
        HYBRID = 'HYBRID', _('Hybrid')
        ELECTRIC = 'ELECTRIC', _('Electric')

    class TransmissionType(models.TextChoices):
        MANUAL = 'MANUAL', _('Manual')
        AUTOMATIC = 'AUTOMATIC', _('Automatic')

    class Status(models.TextChoices):
        AVAILABLE = 'AVAILABLE', _('Available')
        IN_USE = 'IN_USE', _('In Use')
        MAINTENANCE = 'MAINTENANCE', _('In Maintenance')
        OUT_OF_SERVICE = 'OUT_OF_SERVICE', _('Out of Service')

    brand = models.CharField(max_length=100, default='Unknown', verbose_name=_('Brand'))
    model = models.CharField(max_length=100, default='Unknown', verbose_name=_('Model'))
    year = models.IntegerField(default=2000, verbose_name=_('Year'))
    license_plate = models.CharField(max_length=20, unique=True, verbose_name=_('License Plate'))
    vin = models.CharField(max_length=17, unique=True, default='Unknown', verbose_name=_('VIN'))
    color = models.CharField(max_length=50, default='White', verbose_name=_('Color'))
    fuel_type = models.CharField(max_length=20, choices=FuelType.choices, default=FuelType.DIESEL, verbose_name=_('Fuel Type'))
    transmission = models.CharField(max_length=20, choices=TransmissionType.choices, default=TransmissionType.AUTOMATIC, verbose_name=_('Transmission'))
    vehicle_type = models.CharField(max_length=20, choices=VehicleType.choices, default=VehicleType.TRUCK, verbose_name=_('Vehicle Type'))
    mileage = models.IntegerField(default=0, verbose_name=_('Mileage'))
    last_service_date = models.DateField(null=True, blank=True, verbose_name=_('Last Service Date'))
    next_service_date = models.DateField(null=True, blank=True, verbose_name=_('Next Service Date'))
    insurance_expiry = models.DateField(null=True, blank=True, verbose_name=_('Insurance Expiry Date'))
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE, verbose_name=_('Status'))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.license_plate})"

    def is_service_due(self):
        """Check if service is due based on next_service_date."""
        from django.utils import timezone
        if not self.next_service_date:
            return False
        return self.next_service_date <= timezone.now().date()


class VehicleMediaType(models.TextChoices):
    IMAGE = 'IMAGE', _('Image')
    VIDEO = 'VIDEO', _('Video')
    SOUND = 'SOUND', _('Sound')


class VehicleMedia(models.Model):
    vehicle = models.ForeignKey(
        Vehicle, 
        on_delete=models.CASCADE, 
        related_name='media', 
        verbose_name=_('Vehicle')
    )
    media_type = models.CharField(
        max_length=10, 
        choices=VehicleMediaType.choices, 
        verbose_name=_('Media Type')
    )
    file = models.FileField(
        upload_to='vehicle_media/', 
        verbose_name=_('File')
    )
    title = models.CharField(
        max_length=255, 
        blank=True, 
        verbose_name=_('Title')
    )
    description = models.TextField(
        blank=True, 
        verbose_name=_('Description')
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = _('Vehicle Media')
        verbose_name_plural = _('Vehicle Media Gallery')
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_media_type_display()} - {self.vehicle} - {self.title or 'Unnamed'}"
