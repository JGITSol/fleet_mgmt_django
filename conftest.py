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
        # Ensure any leftover test DB file is removed so the test run starts
        # with a fresh database. The project keeps test DB in
        # CarFleetManagement/test_db.sqlite3 when TESTING is enabled.
        try:
            from pathlib import Path
            test_db = Path(__file__).resolve().parent / 'CarFleetManagement' / 'test_db.sqlite3'
            if test_db.exists():
                test_db.unlink()
        except Exception:
            # Non-fatal: if removal fails, let tests proceed and pytest-django
            # will attempt to create/flush the DB. Any exception will surface
            # during test execution if critical.
            pass

# Override the default pytest-django client fixture to use DRF APIClient
from rest_framework.test import APIClient


@pytest.fixture
def api_client():
    """Return a DRF APIClient instance for API tests. Do not override the default
    `client` fixture which provides Django's test Client for template-based tests."""
    return APIClient()
