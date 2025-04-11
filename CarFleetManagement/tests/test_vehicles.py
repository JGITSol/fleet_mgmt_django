import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from vehicles.models import Vehicle

# Import tests from the app-specific test directory
from vehicles.tests.test_models import VehicleTestCase


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_vehicle_status_update(vehicle):
    """Test updating vehicle status."""
    # Test changing status
    vehicle.status = Vehicle.Status.MAINTENANCE
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.status == Vehicle.Status.MAINTENANCE


@pytest.mark.django_db
def test_vehicle_mileage_update(vehicle):
    """Test updating vehicle mileage."""
    # Update mileage
    new_mileage = vehicle.mileage + 1000
    vehicle.mileage = new_mileage
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.mileage == new_mileage


@pytest.mark.django_db
def test_vehicle_service_due(vehicle):
    """Test service due calculation."""
    # Set next service date to yesterday
    yesterday = timezone.now().date() - timedelta(days=1)
    vehicle.next_service_date = yesterday
    vehicle.save()
    
    # Retrieve from DB and verify
    updated_vehicle = Vehicle.objects.get(id=vehicle.id)
    assert updated_vehicle.is_service_due()