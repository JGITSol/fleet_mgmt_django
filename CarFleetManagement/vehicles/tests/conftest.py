from datetime import timedelta

import pytest
from django.utils import timezone


@pytest.fixture
def vehicle(db):
    import uuid
    from CarFleetManagement.vehicles.models import Vehicle
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
        status=Vehicle.Status.AVAILABLE
    )
