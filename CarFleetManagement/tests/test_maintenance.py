import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from maintenance.models import Maintenance

# Import tests from the app-specific test directory if they exist
try:
    from maintenance.tests.test_models import *
except ImportError:
    pass


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_maintenance_creation(maintenance, vehicle):
    """Test maintenance record creation using fixture."""
    # Retrieve from DB and verify
    record = Maintenance.objects.get(vehicle=vehicle)
    assert record.maintenance_type == 'ROUTINE'
    assert record.cost == 50.00
    assert record.odometer_reading == 14500


@pytest.mark.django_db
def test_scheduled_maintenance_creation(scheduled_maintenance, vehicle):
    """Test scheduled maintenance creation using fixture."""
    # Retrieve from DB and verify
    maintenance = Maintenance.objects.get(id=scheduled_maintenance.id)
    assert maintenance.maintenance_type == 'ROUTINE'
    assert maintenance.status == 'SCHEDULED'
    assert maintenance.cost == 200.00


@pytest.mark.django_db
def test_maintenance_str_representation(maintenance):
    """Test string representation of Maintenance."""
    # The string representation depends on the __str__ method implementation
    # This is a basic check that the string representation is not empty
    assert str(maintenance) != ''


@pytest.mark.django_db
def test_maintenance_days_until_scheduled(scheduled_maintenance):
    """Test days until scheduled calculation."""
    # Check that the days_until_scheduled method works for future dates
    if hasattr(scheduled_maintenance, 'days_until_scheduled'):
        days = scheduled_maintenance.days_until_scheduled()
        assert isinstance(days, int)
        # The fixture creates a maintenance scheduled 90 days in the future
        assert days > 0
    
    # Now test with a past date
    yesterday = timezone.now().date() - timedelta(days=1)
    scheduled_maintenance.scheduled_date = yesterday
    scheduled_maintenance.save()
    
    # Verify the days calculation is negative for past dates
    updated_maintenance = Maintenance.objects.get(id=scheduled_maintenance.id)
    if hasattr(updated_maintenance, 'days_until_scheduled'):
        days = updated_maintenance.days_until_scheduled()
        assert isinstance(days, int)
        assert days < 0