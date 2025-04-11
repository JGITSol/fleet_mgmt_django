import pytest
from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from emergency.models import EmergencyContact, EmergencyReport

# Import tests from the app-specific test directory
from emergency.tests.test_models import *


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_emergency_contact_creation(emergency_contact, user_profile):
    """Test emergency contact creation using fixture."""
    # Retrieve from DB and verify
    contact = EmergencyContact.objects.get(user_profile=user_profile)
    assert contact.name == 'Emergency Person'
    assert contact.relationship == 'Family'
    assert contact.phone_number == '+1122334455'


@pytest.mark.django_db
def test_emergency_report_creation(emergency_report, vehicle, user):
    """Test emergency report creation using fixture."""
    # Retrieve from DB and verify
    report = EmergencyReport.objects.get(vehicle=vehicle)
    assert report.incident_type == 'Accident'
    assert report.severity == 'Medium'
    assert report.reporter == user
    assert not report.resolved


@pytest.mark.django_db
def test_emergency_contact_str_representation(emergency_contact):
    """Test string representation of EmergencyContact."""
    expected = f'{emergency_contact.name} ({emergency_contact.relationship})'
    assert str(emergency_contact) == expected


@pytest.mark.django_db
def test_emergency_report_resolution(emergency_report):
    """Test emergency report resolution."""
    # Mark as resolved
    emergency_report.resolved = True
    emergency_report.resolution_date = timezone.now()
    emergency_report.resolution_notes = 'Issue resolved'
    emergency_report.save()
    
    # Verify it's now resolved
    updated_report = EmergencyReport.objects.get(id=emergency_report.id)
    assert updated_report.resolved
    assert updated_report.resolution_notes == 'Issue resolved'
    assert updated_report.resolution_date is not None