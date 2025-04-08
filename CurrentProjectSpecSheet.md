# Fleet Manager Project Specification

## Database Models

### Driver Model
```python
from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from vehicles.models import Vehicle

class DriverStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    INACTIVE = 'INACTIVE', _('Inactive')
    SUSPENDED = 'SUSPENDED', _('Suspended')

class Driver(models.Model):
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=17, blank=True, verbose_name=_('Phone Number'))
    driver_license_number = models.CharField(max_length=20, unique=True, verbose_name=_('Driver License Number'))
    license_expiry_date = models.DateField(verbose_name=_('License Expiry Date'))
    status = models.CharField(max_length=10, choices=DriverStatus.choices, default=DriverStatus.ACTIVE, verbose_name=_('Driver Status'))
    assigned_vehicles = models.ManyToManyField(Vehicle, related_name='assigned_drivers', blank=True, verbose_name=_('Assigned Vehicles'))
    hire_date = models.DateField(verbose_name=_('Hire Date'))
    termination_date = models.DateField(null=True, blank=True, verbose_name=_('Termination Date'))
```

### Vehicle Model
```python
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
```

### Maintenance Model
```python
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
    scheduled_date = models.DateField(verbose_name=_('Scheduled Date'))
    completed_date = models.DateField(null=True, blank=True, verbose_name=_('Completed Date'))
    odometer_reading = models.PositiveIntegerField(validators=[MinValueValidator(0)], verbose_name=_('Odometer Reading'))
    cost = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)], verbose_name=_('Maintenance Cost'))
    service_provider = models.CharField(max_length=100, verbose_name=_('Service Provider'))
    notes = models.TextField(blank=True, verbose_name=_('Additional Notes'))
```

## Serializers

### Driver Serializer
```python
from rest_framework import serializers
from .models import Driver
from vehicles.serializers import VehicleSerializer

class DriverSerializer(serializers.ModelSerializer):
    assigned_vehicles = VehicleSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'phone_number', 'driver_license_number', 'license_expiry_date',
            'status', 'assigned_vehicles', 'hire_date', 'termination_date'
        ]
        read_only_fields = ['id']
```

### Vehicle Serializer
```python
from rest_framework import serializers
from .models import Vehicle

class VehicleSerializer(serializers.ModelSerializer):
    assigned_drivers = DriverNestedSerializer(many=True, read_only=True)
    maintenance_records = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'vin', 'brand', 'model', 'year', 'vehicle_type',
            'license_plate', 'mileage', 'status', 'fuel_type',
            'transmission', 'color', 'last_service_date',
            'next_service_date', 'insurance_expiry', 'created_at',
            'updated_at', 'assigned_drivers', 'maintenance_records'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
```

### Maintenance Serializer
```python
from rest_framework import serializers
from .models import Maintenance
from vehicles.serializers import VehicleSerializer

class MaintenanceSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    days_until_scheduled = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = [
            'id', 'vehicle', 'vehicle_details', 'maintenance_type',
            'status', 'description', 'scheduled_date', 'completed_date',
            'odometer_reading', 'cost', 'service_provider', 'notes',
            'days_until_scheduled'
        ]
        read_only_fields = ['id']
```

## Admin Configurations

### Driver Admin
```python
from django.contrib import admin
from .models import Driver

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'driver_license_number', 'status', 'license_expiry_date')
    list_filter = ('status', 'license_expiry_date', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'driver_license_number')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('id',)
    filter_horizontal = ('assigned_vehicles',)
```

### Vehicle Admin
```python
from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'year', 'vehicle_type', 'status', 'mileage')
    list_filter = ('vehicle_type', 'status', 'brand', 'year')
    search_fields = ('license_plate', 'vin', 'brand', 'model')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
```

### Maintenance Admin
```python
from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_type', 'status', 'scheduled_date', 'cost')
    list_filter = ('maintenance_type', 'status', 'scheduled_date')
    search_fields = ('vehicle__vin', 'vehicle__license_plate', 'description', 'service_provider')
    ordering = ('-scheduled_date',)
    readonly_fields = ('id',)
    raw_id_fields = ('vehicle',)
```