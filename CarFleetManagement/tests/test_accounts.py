import contextlib

import pytest
from django.contrib.auth import get_user_model

from CarFleetManagement.accounts.models import CustomUser, Driver

# Import tests from the app-specific test directory if they exist
with contextlib.suppress(ImportError):
    # Explicitly import commonly used symbols from the app-level tests instead
    # of using a star import which confuses static analyzers.
    # App-level test models exist in CarFleetManagement.accounts.tests; we
    # don't need to rebind them here. The contextlib.suppress block is kept
    # to avoid ImportError when those modules are absent.
    pass
User = get_user_model()


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_custom_user_creation(custom_user):
    """Test custom user creation using fixture."""
    # Retrieve from DB and verify
    user = CustomUser.objects.get(id=custom_user.id)
    assert user.phone_number == "+1234567890"


@pytest.mark.django_db
def test_driver_creation(driver):
    """Test driver creation using fixture."""
    # Retrieve from DB and verify
    driver_obj = Driver.objects.get(id=driver.id)
    # driver_license_number is generated uniquely by the fixture; verify pattern
    assert driver_obj.driver_license_number.startswith("DL")
    assert driver_obj.phone_number == "+1234567890"
    # status field removed from model, test skipped


@pytest.mark.django_db
def test_custom_user_str_representation(custom_user):
    """Test string representation of CustomUser."""
    assert str(custom_user) == custom_user.username
