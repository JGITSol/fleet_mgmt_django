"""
Run tests with authentication patch applied.

This script applies the authentication patch from auth_utils.py and runs the tests.
The patch provides a comprehensive solution for authentication in tests by:
1. Patching permission classes to handle both authenticated and unauthenticated test cases
2. Providing utilities to create test users with different roles
3. Generating JWT tokens and authenticating test clients
4. Supporting context managers and decorators for applying authentication in tests
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

# Import the authentication utilities
from tests.auth_utils import AuthUtils

# Apply the patch
print("Applying authentication patch...")
AuthUtils.apply_jwt_patch()
print("Patch applied successfully!")

# Run the tests
print("Running tests...")
try:
    # Run pytest with verbose output
    exit_code = pytest.main(["-v"])
    
    if exit_code == 0:
        print("\n✅ All tests passed successfully!")
    else:
        print(f"\n❌ Some tests failed. Exit code: {exit_code}")
        
finally:
    # Restore original permission classes
    print("Restoring original permission classes...")
    AuthUtils.restore_jwt_patch()
    print("Original permission classes restored.")
