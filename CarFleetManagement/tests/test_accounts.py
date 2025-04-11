import pytest
from django.test import TestCase
from django.contrib.auth import get_user_model

from accounts.models import CustomUser, Driver

# Import tests from the app-specific test directory if they exist
try:
    from accounts.tests.test_models import *
except ImportError:
    pass

User = get_user_model()


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_custom_user_creation(custom_user):
    """Test custom user creation using fixture."""
    # Retrieve from DB and verify
    user = CustomUser.objects.get(id=custom_user.id)
    assert user.phone_number == '+1234567890'


@pytest.mark.django_db
def test_driver_creation(driver):
    """Test driver creation using fixture."""
    # Retrieve from DB and verify
    driver_obj = Driver.objects.get(id=driver.id)
    assert driver_obj.driver_license_number == 'DL12345678'
    assert driver_obj.phone_number == '+1234567890'
    assert driver_obj.status == 'ACTIVE'


@pytest.mark.django_db
def test_custom_user_str_representation(custom_user):
    """Test string representation of CustomUser."""
    assert str(custom_user) == custom_user.username


@pytest.mark.django_db
def test_driver_license_expiry(driver):
    """Test driver license expiry check."""
    # License is valid (future expiry date)
    from django.utils import timezone
    assert driver.license_expiry_date > timezone.now().date()
    
    # Update to expired license
    from datetime import timedelta
    
    driver.license_expiry_date = timezone.now().date() - timedelta(days=1)
    driver.save()
    
    # Verify it's now expired
    updated_driver = Driver.objects.get(id=driver.id)
    assert updated_driver.license_expiry_date < timezone.now().date()