"""
Pytest configuration file for Django settings.
This ensures Django settings are properly configured before tests run.
"""
import os

import pytest

# Add the project directory to the Python path
# project_dir = os.path.dirname(os.path.abspath(__file__))
# sys.path.insert(0, project_dir)

# The actual Django app is in the CarFleetManagement subdirectory
# django_app_dir = os.path.join(project_dir, 'CarFleetManagement')
# sys.path.insert(0, django_app_dir)

# Set dummy OpenRouter API key for tests
os.environ['OPENROUTER_API_KEY'] = 'test-api-key'
# Configure Django settings before any tests run
# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

# Setup Django
# django.setup()

# Define a pytest fixture to provide a database transaction for tests
@pytest.fixture(scope='session')
def django_db_setup(django_db_blocker):
    """Configure Django database for testing."""
    with django_db_blocker.unblock():
        # Here you could load fixtures or perform other database setup
        pass

# Override the default pytest-django client fixture to use DRF APIClient
from rest_framework.test import APIClient


@pytest.fixture
def client():
    """Return a DRF APIClient instance instead of Django test Client."""
    return APIClient()
