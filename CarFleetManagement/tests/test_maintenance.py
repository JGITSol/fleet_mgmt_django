import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from maintenance.models import MaintenanceRecord, ServiceSchedule

# Import tests from the app-specific test directory
from maintenance.tests.test_models import *


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_maintenance_record_creation(maintenance_record, vehicle):
    """Test maintenance record creation using fixture."""
    # Retrieve from DB and verify
    record = MaintenanceRecord.objects.get(vehicle=vehicle)
    assert record.service_type == 'Oil Change'
    assert record.cost == 50.00
    assert record.mileage == 14500


@pytest.mark.django_db
def test_service_schedule_creation(service_schedule, vehicle):
    """Test service schedule creation using fixture."""
    # Retrieve from DB and verify
    schedule = ServiceSchedule.objects.get(vehicle=vehicle)
    assert schedule.service_type == 'Regular Maintenance'
    assert schedule.interval_months == 6
    assert schedule.interval_miles == 5000


@pytest.mark.django_db
def test_maintenance_record_str_representation(maintenance_record):
    """Test string representation of MaintenanceRecord."""
    expected = f'{maintenance_record.vehicle} - {maintenance_record.service_type} on {maintenance_record.service_date}'
    assert str(maintenance_record) == expected


@pytest.mark.django_db
def test_service_schedule_due_check(service_schedule):
    """Test service schedule due check."""
    # Set next service date to yesterday to make it due
    yesterday = timezone.now().date() - timedelta(days=1)
    service_schedule.next_service_date = yesterday
    service_schedule.save()
    
    # Verify it's now due
    updated_schedule = ServiceSchedule.objects.get(id=service_schedule.id)
    assert updated_schedule.is_service_due()