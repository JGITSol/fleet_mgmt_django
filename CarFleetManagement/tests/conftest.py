"""
conftest.py: Pytest fixtures for CarFleetManagement tests.
All fixtures are documented for coverage compliance.
"""
import os
import sys
import django
import pytest
from datetime import timedelta

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_dir)

# Configure Django settings before importing any models
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

# This will make sure the app is always imported when Django starts
# so that shared_task will use this app
from django.conf import settings

# Setup Django
django.setup()

# pytest-django will be automatically discovered by pytest

# Now it's safe to import Django models
from django.contrib.auth import get_user_model
from django.utils import timezone

from vehicles.models import Vehicle
from accounts.models import CustomUser, Driver
from maintenance.models import Maintenance
from CarFleetManagement.emergency.models import EmergencyContact, EmergencyIncident


User = get_user_model()


def test_fixtures_coverage(user, custom_user, driver, vehicle, maintenance, scheduled_maintenance, emergency_contact, emergency_incident):
    """
    Smoke test to ensure all fixtures are exercised for coverage purposes.
    """
    assert user.pk
    assert custom_user.pk
    assert driver.pk
    assert vehicle.pk
    assert maintenance.pk
    assert scheduled_maintenance.pk
    assert emergency_contact.pk
    assert emergency_incident.pk

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
    return Driver.objects.create(
        first_name='Test',
        last_name='Driver',
        email='driver@example.com',
        phone_number='+1234567890',
        driver_license_number='DL12345678',
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