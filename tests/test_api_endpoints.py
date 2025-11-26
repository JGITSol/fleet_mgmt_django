#!/usr/bin/env python3
"""
API Endpoint Testing Script for Car Fleet Management System

This script tests all API endpoints to ensure they're working correctly.
Run this after starting the Django development server.
"""

import sys
from urllib.parse import urljoin

import requests

# Configuration
BASE_URL = "http://localhost:8000"
API_BASE = f"{BASE_URL}/api/"

# Test credentials (you may need to create a test user)
TEST_USER = {"username": "testuser", "password": "testpass123"}


class APITester:
    def __init__(self, base_url):
        self.base_url = base_url
        self.session = requests.Session()
        self.access_token = None

    def log(self, message, status="INFO"):
        print(f"[{status}] {message}")

    def test_endpoint(self, method, endpoint, data=None, auth_required=True):
        """Test a single API endpoint"""
        url = urljoin(self.base_url, endpoint)
        headers = {}

        if auth_required and self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"

        try:
            if method.upper() == "GET":
                response = self.session.get(url, headers=headers)
            elif method.upper() == "POST":
                headers["Content-Type"] = "application/json"
                response = self.session.post(url, headers=headers, json=data)
            elif method.upper() == "PUT":
                headers["Content-Type"] = "application/json"
                response = self.session.put(url, headers=headers, json=data)
            elif method.upper() == "DELETE":
                response = self.session.delete(url, headers=headers)
            else:
                self.log(f"Unsupported method: {method}", "ERROR")
                return False

            self.log(f"{method} {endpoint} -> {response.status_code}")

            if response.status_code < 400:
                return True
            else:
                self.log(f"Error response: {response.text[:200]}", "WARN")
                return False

        except requests.exceptions.ConnectionError:
            self.log(f"Connection failed to {url}", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error testing {endpoint}: {str(e)}", "ERROR")
            return False

    def authenticate(self):
        """Attempt to authenticate and get JWT token"""
        self.log("Attempting authentication...")

        # Try to login with test credentials
        login_data = TEST_USER
        response = self.session.post(
            urljoin(self.base_url, "api/auth/login/"), json=login_data
        )

        if response.status_code == 200:
            data = response.json()
            self.access_token = data.get("access")
            self.log("Authentication successful", "SUCCESS")
            return True
        else:
            self.log("Authentication failed - testing without auth", "WARN")
            return False

    def test_all_endpoints(self):
        """Test all API endpoints"""
        self.log("Starting API endpoint tests...")

        # Test basic connectivity
        if not self.test_endpoint("GET", "", auth_required=False):
            self.log("Cannot connect to API base URL", "ERROR")
            return False

        # Attempt authentication
        self.authenticate()

        # Define endpoints to test
        endpoints = [
            # API Root
            ("GET", "api/", False),
            # Authentication endpoints
            ("POST", "api/auth/register/", False),
            ("POST", "api/auth/login/", False),
            ("GET", "api/auth/profile/", True),
            ("POST", "api/auth/validate-token/", False),
            # Vehicle endpoints
            ("GET", "api/vehicles/", True),
            ("POST", "api/vehicles/", True),
            # Driver endpoints
            ("GET", "api/drivers/", True),
            ("POST", "api/drivers/", True),
            # Maintenance endpoints
            ("GET", "api/maintenance/", True),
            ("POST", "api/maintenance/", True),
            # Emergency endpoints
            ("GET", "api/emergencies/", True),
            ("POST", "api/emergencies/", True),
            ("GET", "api/emergencies/responses/", True),
            ("POST", "api/emergencies/responses/", True),
            # AI endpoints
            ("POST", "api/screenshots/analyze/", True),
            ("POST", "api/screenshots/batch-analyze/", True),
            ("POST", "api/screenshots/generate-report/", True),
        ]

        # Test each endpoint
        passed = 0
        failed = 0

        for method, endpoint, auth_required in endpoints:
            if self.test_endpoint(method, endpoint, auth_required=auth_required):
                passed += 1
            else:
                failed += 1

        # Summary
        total = passed + failed
        self.log("\nTest Summary:")
        self.log(f"Total endpoints tested: {total}")
        self.log(f"Passed: {passed}")
        self.log(f"Failed: {failed}")
        self.log(f"Success rate: {(passed / total) * 100:.1f}%")

        return failed == 0


def main():
    """Main function"""
    print("Car Fleet Management API Endpoint Tester")
    print("=" * 50)

    # Check if server is running
    try:
        requests.get(BASE_URL, timeout=5)
        print(f"✓ Server is running at {BASE_URL}")
    except requests.exceptions.ConnectionError:
        print(f"✗ Cannot connect to server at {BASE_URL}")
        print("Please make sure the Django development server is running:")
        print("  python manage.py runserver")
        sys.exit(1)

    # Run tests
    tester = APITester(BASE_URL)
    success = tester.test_all_endpoints()

    if success:
        print("\n🎉 All API endpoints are working correctly!")
        sys.exit(0)
    else:
        print("\n⚠️  Some API endpoints have issues. Check the logs above.")
        sys.exit(1)


if __name__ == "__main__":
    main()
