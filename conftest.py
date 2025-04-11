"""
Pytest configuration file for Django settings.
This ensures Django settings are properly configured before tests run.
"""
import os
import sys
import pytest
import django
from django.conf import settings

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# The actual Django app is in the CarFleetManagement subdirectory
django_app_dir = os.path.join(project_dir, 'CarFleetManagement')
sys.path.insert(0, django_app_dir)

# Configure Django settings before any tests run
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.car_fleet_manager.settings")

# Setup Django
django.setup()

# Define a pytest fixture to provide a database transaction for tests
@pytest.fixture(scope='function')
def django_db_setup(django_db_blocker):
    """Configure Django database for testing."""
    with django_db_blocker.unblock():
        # Here you could load fixtures or perform other database setup
        pass
