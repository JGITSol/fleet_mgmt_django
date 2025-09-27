#!/usr/bin/env python
"""
Test Development Credentials
============================

This script tests the development credentials by making API calls.
"""

import sys

import requests


def test_credentials():
    """Test the development credentials."""

    base_url = "http://localhost:8000"

    print("🧪 Testing Development Credentials")
    print("=" * 40)

    # Test admin credentials
    print("Testing admin credentials...")
    admin_data = {"username": "admin", "password": "admin123!"}

    try:
        # Test login endpoint
        response = requests.post(f"{base_url}/api/auth/login/", json=admin_data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Admin login successful")
            print(
                f"   Access token received: {token_data.get('access', 'N/A')[:20]}..."
            )
        else:
            print(f"❌ Admin login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except requests.exceptions.ConnectionError:
        print(
            "❌ Cannot connect to server. Make sure the development server is running."
        )
        print("   Run: python start_dev_server.py")
        return False
    except Exception as e:
        print(f"❌ Error testing admin credentials: {e}")

    # Test regular user credentials
    print("\nTesting regular user credentials...")
    user_data = {"username": "testuser", "password": "user123!"}

    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=user_data)
        if response.status_code == 200:
            token_data = response.json()
            print("✅ Regular user login successful")
            print(
                f"   Access token received: {token_data.get('access', 'N/A')[:20]}..."
            )
        else:
            print(f"❌ Regular user login failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing regular user credentials: {e}")

    # Test web interface
    print("\nTesting web interface...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("✅ Web interface accessible")
        else:
            print(f"❌ Web interface error: {response.status_code}")
    except Exception as e:
        print(f"❌ Error testing web interface: {e}")

    print("\n" + "=" * 40)
    print("🎯 Test Summary:")
    print("   - Admin credentials: admin / admin123!")
    print("   - User credentials: testuser / user123!")
    print("   - Login URL: http://localhost:8000/accounts/login/")
    print("   - Admin Panel: http://localhost:8000/admin/")
    print("   - API Docs: http://localhost:8000/api/schema/swagger-ui/")

    return True


if __name__ == "__main__":
    success = test_credentials()
    sys.exit(0 if success else 1)
