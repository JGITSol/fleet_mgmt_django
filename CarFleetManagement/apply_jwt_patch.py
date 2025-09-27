"""
Apply JWT patch and run tests.

This script applies the JWT authentication patch and runs the tests.
"""
import os
import sys

import django
import pytest

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

# Setup Django
django.setup()

# Import the JWT patch
from tests.jwt_test_patch import patch_permissions_for_testing

# Apply the patch
print("Applying JWT authentication patch...")
patch_permissions_for_testing()
print("Patch applied successfully!")

# Run the tests
print("Running tests...")
pytest.main(["-v"])
