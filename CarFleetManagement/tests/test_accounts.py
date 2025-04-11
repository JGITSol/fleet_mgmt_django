import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import UserProfile, DriverLicense

# Import tests from the app-specific test directory
from accounts.tests.test_models import *

User = get_user_model()


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_user_profile_creation(user_profile):
    """Test user profile creation using fixture."""
    # Retrieve from DB and verify
    profile = UserProfile.objects.get(user=user_profile.user)
    assert profile.phone_number == '+1234567890'
    assert profile.address == '123 Test St, Test City'
    assert profile.employee_id == 'EMP12345'


@pytest.mark.django_db
def test_driver_license_creation(driver_license):
    """Test driver license creation using fixture."""
    # Retrieve from DB and verify
    license = DriverLicense.objects.get(license_number='DL12345678')
    assert license.license_class == 'B'
    assert str(license.expiry_date) == '2025-01-01'
    assert license.issuing_authority == 'Test DMV'


@pytest.mark.django_db
def test_user_profile_str_representation(user_profile):
    """Test string representation of UserProfile."""
    assert str(user_profile) == f'Profile for {user_profile.user.username}'


@pytest.mark.django_db
def test_driver_license_expiry_check(driver_license, user_profile):
    """Test driver license expiry check."""
    # License is valid (future expiry date)
    assert not driver_license.is_expired()
    
    # Update to expired license
    from django.utils import timezone
    from datetime import timedelta
    
    driver_license.expiry_date = timezone.now().date() - timedelta(days=1)
    driver_license.save()
    
    # Verify it's now expired
    updated_license = DriverLicense.objects.get(id=driver_license.id)
    assert updated_license.is_expired()