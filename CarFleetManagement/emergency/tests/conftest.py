import pytest
from django.contrib.auth import get_user_model
# Model imports moved into fixture functions

@pytest.fixture
def custom_user(db):
    User = get_user_model()
    return User.objects.create_user(username='testuser', email='test@example.com', password='pass1234')

@pytest.fixture
def vehicle(db):
    from CarFleetManagement.vehicles.models import Vehicle
    return Vehicle.objects.create(
        brand='Toyota', model='Camry', year=2020, license_plate='ABC-123', vin='VIN123', status='AVAILABLE'
    )

@pytest.fixture
def driver(db):
    from CarFleetManagement.accounts.models import Driver
    return Driver.objects.create(
        first_name='John',
        last_name='Doe',
        driver_license_number='D1234567',
        phone_number='555-555-5555',
        email='driver@example.com'
    )

@pytest.fixture
def emergency_contact(db, custom_user):
    from CarFleetManagement.emergency.models import EmergencyContact
    return EmergencyContact.objects.create(user=custom_user, name='Jane Doe', phone_number='1234567890', relationship='Spouse')

@pytest.fixture
def emergency_incident(db, vehicle, driver, custom_user):
    from CarFleetManagement.emergency.models import EmergencyIncident
    return EmergencyIncident.objects.create(
        vehicle=vehicle,
        driver=driver,
        reported_by=custom_user,
        emergency_type='ACCIDENT',
        status='REPORTED',
        location='Test Location',
        latitude=10.0,
        longitude=20.0,
        description='Test description'
    )
