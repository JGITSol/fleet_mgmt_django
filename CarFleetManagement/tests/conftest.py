import os
import sys
import django
import pytest
from datetime import timedelta

# Configure Django settings before importing any models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "car_fleet_manager.settings")
django.setup()

# Now it's safe to import Django models
from django.contrib.auth import get_user_model
from django.utils import timezone

from vehicles.models import Vehicle
from accounts.models import CustomUser, Driver
from maintenance.models import Maintenance
from emergency.models import EmergencyContact, EmergencyIncident


User = get_user_model()


@pytest.fixture
def user():
    """Create and return a test user."""
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpassword'
    )


@pytest.fixture
def custom_user(user):
    """Create and return a test custom user."""
    from accounts.models import UserRole
    role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER, defaults={'description': 'Driver role'})
    user.role = role
    user.phone_number = '+1234567890'
    user.save()
    return user


@pytest.fixture
def driver(custom_user):
    """Create and return a test driver."""
    today = timezone.now().date()
    return Driver.objects.create(
        user=custom_user,
        first_name='Test',
        last_name='Driver',
        email='driver@example.com',
        phone_number='+1234567890',
        driver_license_number='DL12345678',
        license_expiry_date=today + timedelta(days=365),
        status='ACTIVE',
        hire_date=today - timedelta(days=90)
    )


@pytest.fixture
def vehicle():
    """Create and return a test vehicle."""
    today = timezone.now().date()
    next_service = today + timedelta(days=90)
    insurance_expiry = today + timedelta(days=365)
    
    return Vehicle.objects.create(
        brand='Toyota',
        model='Camry',
        year=2022,
        license_plate='ABC-123',
        vin='1HGCM82633A123456',
        color='Blue',
        fuel_type=Vehicle.FuelType.HYBRID,
        transmission=Vehicle.TransmissionType.AUTOMATIC,
        vehicle_type=Vehicle.VehicleType.SUV,
        mileage=15000,
        last_service_date=today - timedelta(days=90),
        next_service_date=next_service,
        insurance_expiry=insurance_expiry,
        status=Vehicle.Status.AVAILABLE
    )


@pytest.fixture
def maintenance(vehicle):
    """Create and return a test maintenance record."""
    return Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='COMPLETED',
        description='Regular oil change and filter replacement',
        scheduled_date=timezone.now().date() - timedelta(days=30),
        completed_date=timezone.now().date() - timedelta(days=30),
        odometer_reading=14500,
        cost=50.00,
        service_provider='Test Mechanic',
        notes='Everything looks good'
    )


@pytest.fixture
def scheduled_maintenance(vehicle):
    """Create and return a test scheduled maintenance."""
    return Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='SCHEDULED',
        description='Full vehicle inspection and maintenance',
        scheduled_date=timezone.now().date() + timedelta(days=90),
        odometer_reading=15000,
        cost=200.00,
        service_provider='Test Service Center',
        notes='Includes oil change, filter replacement, and inspection'
    )


@pytest.fixture
def emergency_contact(custom_user):
    """Create and return a test emergency contact."""
    return EmergencyContact.objects.create(
        user=custom_user,
        name='Emergency Person',
        relationship='Family',
        phone_number='+1122334455'
    )


@pytest.fixture
def emergency_incident(vehicle, custom_user, driver):
    """Create and return a test emergency incident."""
    return EmergencyIncident.objects.create(
        vehicle=vehicle,
        driver=driver,
        reported_by=custom_user,
        emergency_type='ACCIDENT',
        status='REPORTED',
        location='Intersection of Test St and Example Ave',
        description='Minor collision with another vehicle'
    )