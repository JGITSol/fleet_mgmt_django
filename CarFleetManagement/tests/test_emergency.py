import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from emergency.models import EmergencyContact, EmergencyIncident

# Import tests from the app-specific test directory if they exist
try:
    from emergency.tests.test_models import *
except ImportError:
    pass


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_emergency_contact_creation(emergency_contact, custom_user):
    """Test emergency contact creation using fixture."""
    # Retrieve from DB and verify
    contact = EmergencyContact.objects.get(user=custom_user)
    assert contact.name == 'Emergency Person'
    assert contact.relationship == 'Family'
    assert contact.phone_number == '+1122334455'


@pytest.mark.django_db
def test_emergency_incident_creation(emergency_incident, vehicle, custom_user):
    """Test emergency incident creation using fixture."""
    # Retrieve from DB and verify
    incident = EmergencyIncident.objects.get(vehicle=vehicle)
    assert incident.emergency_type == 'ACCIDENT'
    assert incident.status == 'REPORTED'
    assert incident.reported_by == custom_user
    assert incident.location == 'Intersection of Test St and Example Ave'


@pytest.mark.django_db
def test_emergency_contact_str_representation(emergency_contact):
    """Test string representation of EmergencyContact."""
    # The string representation depends on the __str__ method implementation
    # This is a basic check that the string representation is not empty
    assert str(emergency_contact) != ''


@pytest.mark.django_db
def test_emergency_incident_status_update(emergency_incident):
    """Test emergency incident status update."""
    # Mark as resolved
    emergency_incident.status = 'RESOLVED'
    emergency_incident.resolved_time = timezone.now()
    emergency_incident.save()
    
    # Verify it's now resolved
    updated_incident = EmergencyIncident.objects.get(id=emergency_incident.id)
    assert updated_incident.status == 'RESOLVED'
    assert updated_incident.resolved_time is not None