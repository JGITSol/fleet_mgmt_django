import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

from vehicles.models import Vehicle
from accounts.models import UserProfile, DriverLicense
from maintenance.models import MaintenanceRecord, ServiceSchedule
from emergency.models import EmergencyContact, EmergencyReport


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
def user_profile(user):
    """Create and return a test user profile."""
    return UserProfile.objects.create(
        user=user,
        phone_number='+1234567890',
        address='123 Test St, Test City',
        emergency_contact_name='Emergency Contact',
        emergency_contact_phone='+0987654321',
        employee_id='EMP12345',
        department='IT',
        position='Developer'
    )


@pytest.fixture
def driver_license(user_profile):
    """Create and return a test driver license."""
    return DriverLicense.objects.create(
        user_profile=user_profile,
        license_number='DL12345678',
        license_class='B',
        issue_date='2020-01-01',
        expiry_date='2025-01-01',
        issuing_authority='Test DMV',
        restrictions='None'
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
def maintenance_record(vehicle):
    """Create and return a test maintenance record."""
    return MaintenanceRecord.objects.create(
        vehicle=vehicle,
        service_date=timezone.now().date() - timedelta(days=30),
        service_type='Oil Change',
        description='Regular oil change and filter replacement',
        cost=50.00,
        mileage=14500,
        performed_by='Test Mechanic',
        notes='Everything looks good'
    )


@pytest.fixture
def service_schedule(vehicle):
    """Create and return a test service schedule."""
    return ServiceSchedule.objects.create(
        vehicle=vehicle,
        service_type='Regular Maintenance',
        description='Full vehicle inspection and maintenance',
        interval_months=6,
        interval_miles=5000,
        last_service_date=timezone.now().date() - timedelta(days=90),
        next_service_date=timezone.now().date() + timedelta(days=90),
        estimated_cost=200.00,
        notes='Includes oil change, filter replacement, and inspection'
    )


@pytest.fixture
def emergency_contact(user_profile):
    """Create and return a test emergency contact."""
    return EmergencyContact.objects.create(
        user_profile=user_profile,
        name='Emergency Person',
        relationship='Family',
        phone_number='+1122334455',
        email='emergency@example.com',
        address='456 Emergency St, Safety City'
    )


@pytest.fixture
def emergency_report(vehicle, user):
    """Create and return a test emergency report."""
    return EmergencyReport.objects.create(
        vehicle=vehicle,
        reporter=user,
        incident_date=timezone.now(),
        incident_type='Accident',
        description='Minor collision with another vehicle',
        location='Intersection of Test St and Example Ave',
        severity='Medium',
        actions_taken='Called insurance, took photos',
        resolved=False
    )