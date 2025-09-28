import uuid

import pytest
from django.contrib.auth import get_user_model

# Model imports moved into fixture functions


@pytest.fixture
def custom_user(db):
    User = get_user_model()
    unique_username = f"fixture_user_{uuid.uuid4().hex[:8]}"
    from conftest import TEST_PASSWORD
    return User.objects.create_user(
        username=unique_username, email=f"{unique_username}@example.com", password=TEST_PASSWORD
    )


@pytest.fixture
def vehicle(db):
    from CarFleetManagement.vehicles.models import Vehicle

    return Vehicle.objects.create(
        brand="Toyota", model="Camry", year=2020, license_plate="ABC-123", vin="VIN123", status="AVAILABLE"
    )


@pytest.fixture
def driver(db):
    from django.utils import timezone

    from CarFleetManagement.accounts.models import Driver

    return Driver.objects.create(
        first_name="John",
        last_name="Doe",
        driver_license_number=f"D{int(timezone.now().timestamp())}",
        phone_number="555-555-5555",
        email="driver@example.com",
        license_expiry_date=timezone.now().date(),
        hire_date=timezone.now().date(),
    )


@pytest.fixture
def emergency_contact(db, custom_user):
    from CarFleetManagement.emergency.models import EmergencyContact

    return EmergencyContact.objects.create(
        user=custom_user, name="Jane Doe", phone_number="1234567890", relationship="Spouse"
    )


@pytest.fixture
def emergency_incident(db, vehicle, driver, custom_user):
    from CarFleetManagement.emergency.models import EmergencyIncident

    return EmergencyIncident.objects.create(
        vehicle=vehicle,
        driver=driver,
        reported_by=custom_user,
        emergency_type="ACCIDENT",
        status="REPORTED",
        location="Test Location",
        latitude=10.0,
        longitude=20.0,
        description="Test description",
    )
