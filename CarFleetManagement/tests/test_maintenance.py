
import pytest
from django.utils import timezone

from CarFleetManagement.maintenance.models import Maintenance
from CarFleetManagement.vehicles.models import Vehicle


@pytest.mark.django_db
def test_maintenance_creation():
    """Test maintenance record creation."""
    # Create test vehicle
    vehicle = Vehicle.objects.create(
        brand='Test Brand',
        model='Test Model',
        year=2022,
        license_plate='TEST123',
        vin='TEST12345678901234',
        status='AVAILABLE'
    )

    # Create test maintenance
    maintenance = Maintenance.objects.create(
        vehicle=vehicle,
        maintenance_type='ROUTINE',
        status='COMPLETED',
        description='Test maintenance',
        scheduled_date=timezone.now().date(),
        completed_date=timezone.now().date(),
        odometer_reading=10000,
        cost=50.00,
        service_provider='Test Provider',
        notes='Test notes'
    )

    # Verify the maintenance was created
    assert maintenance.id is not None
    assert maintenance.vehicle == vehicle
    assert maintenance.maintenance_type == 'ROUTINE'
    assert maintenance.cost == 50.00
