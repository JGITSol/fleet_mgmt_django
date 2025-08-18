import pytest
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

from CarFleetManagement.accounts.models import CustomUser, Driver

# Import tests from the app-specific test directory if they exist
try:
    from CarFleetManagement.accounts.tests.test_models import *
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
    # status field removed from model, test skipped


@pytest.mark.django_db
def test_custom_user_str_representation(custom_user):
    """Test string representation of CustomUser."""
    assert str(custom_user) == custom_user.username

