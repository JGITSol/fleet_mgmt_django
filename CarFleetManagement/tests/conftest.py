"""
conftest.py: Pytest fixtures for CarFleetManagement tests.
All fixtures are documented for coverage compliance.
"""
import os
import uuid
from datetime import timedelta

import pytest

# Avoid importing or calling django.setup() at module import time so linters
# don't flag E402. pytest-django will set up Django when tests run. Move
# imports that require Django into fixtures/functions below.

# A single test password used in fixtures to avoid repeated hard-coded literals.
# Allow override via env to avoid hard-coded secrets in some environments.
TEST_PASSWORD = os.environ.get("TEST_PASSWORD", "TestPassword123!")


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
    # Create a uniquely named fixture user to avoid colliding with tests that
    # create their own 'testuser' usernames. Import Django models locally so
    # module-level imports/ django.setup() are not required.
    import django
    from django.contrib.auth import get_user_model

    django.setup()
    User = get_user_model()

    unique_username = f"fixture_user_{uuid.uuid4().hex[:8]}"
    user = User.objects.create_user(
        username=unique_username,
        email=f"{unique_username}@example.com",
        password=TEST_PASSWORD,
    )
    return user


@pytest.fixture
def custom_user(user):
    """Create and return a test custom user."""
    from CarFleetManagement.accounts.models import UserRole
    role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER, defaults={'description': 'Driver role'})
    user.role = role
    user.phone_number = '+1234567890'
    user.save()
    return user


@pytest.fixture
def driver(custom_user):
    """Create and return a test driver."""
    # Add license_expiry_date for compatibility with older migrations that
    # still enforce NOT NULL on this column.
    import django
    from django.utils import timezone

    from CarFleetManagement.accounts.models import Driver

    django.setup()
    return Driver.objects.create(
        first_name='Test',
        last_name='Driver',
        email='driver@example.com',
        phone_number='+1234567890',
        driver_license_number=f'DL{timezone.now().timestamp():.0f}',
        license_expiry_date=timezone.now().date(),
        hire_date=timezone.now().date(),
    )


@pytest.fixture
def vehicle():
    """Create and return a test vehicle."""
    import uuid
    import django
    from django.utils import timezone

    from CarFleetManagement.vehicles.models import Vehicle

    django.setup()
    today = timezone.now().date()
    next_service = today + timedelta(days=90)
    insurance_expiry = today + timedelta(days=365)
    return Vehicle.objects.create(
        brand='Toyota',
        model='Camry',
        year=2022,
        license_plate=f'ABC-{uuid.uuid4().hex[:6].upper()}',
        vin=f'1HGCM82633A{uuid.uuid4().hex[:6].upper()}',
        color='Blue',
        fuel_type=Vehicle.FuelType.HYBRID,
        transmission=Vehicle.TransmissionType.AUTOMATIC,
        vehicle_type=Vehicle.VehicleType.SUV,
        mileage=15000,
        last_service_date=today - timedelta(days=90),
        next_service_date=next_service,
        insurance_expiry=insurance_expiry,
        status=Vehicle.Status.AVAILABLE,
    )


@pytest.fixture
def maintenance(vehicle):
    """Create and return a test maintenance record."""
    import django
    from django.utils import timezone

    from CarFleetManagement.maintenance.models import Maintenance

    django.setup()
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
        notes='Everything looks good',
    )


@pytest.fixture
def scheduled_maintenance(vehicle):
    """Create and return a test scheduled maintenance."""
    import django
    from django.utils import timezone

    from CarFleetManagement.maintenance.models import Maintenance

    django.setup()
    return Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='SCHEDULED',
        description='Full vehicle inspection and maintenance',
        scheduled_date=timezone.now().date() + timedelta(days=90),
        odometer_reading=15000,
        cost=200.00,
        service_provider='Test Service Center',
        notes='Includes oil change, filter replacement, and inspection',
    )


@pytest.fixture
def emergency_contact(custom_user):
    """Create and return a test emergency contact."""
    import django

    from CarFleetManagement.emergency.models import EmergencyContact

    django.setup()
    return EmergencyContact.objects.create(
        user=custom_user,
        name='Emergency Person',
        relationship='Family',
        phone_number='+1122334455',
    )


@pytest.fixture
def emergency_incident(vehicle, custom_user, driver):
    """Create and return a test emergency incident."""
    import django

    from CarFleetManagement.emergency.models import EmergencyIncident

    django.setup()
    return EmergencyIncident.objects.create(
        vehicle=vehicle,
        driver=driver,
        reported_by=custom_user,
        emergency_type='ACCIDENT',
        status='REPORTED',
        location='Intersection of Test St and Example Ave',
        description='Minor collision with another vehicle',
    )
