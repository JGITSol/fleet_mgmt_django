import pytest
from vehicles.models import Vehicle
from django.utils import timezone
from datetime import timedelta

@pytest.fixture
def vehicle(db):
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
