#!/usr/bin/env python3
"""
Quick URL accessibility test for Car Fleet Management System
"""

import requests


def test_urls():
    base_url = "http://localhost:8000"

    # Test URLs
    urls = [
        ("/", "Home Page"),
        ("/admin/", "Admin"),
        ("/api/", "API Root"),
        ("/accounts/login/", "Login"),
        ("/accounts/register/", "Register"),
        ("/vehicles/", "Vehicles"),
        ("/maintenance/", "Maintenance"),
        ("/emergency/", "Emergency"),
    ]

    print("Testing URL accessibility...")
    print("=" * 50)

    for url, name in urls:
        try:
            response = requests.get(f"{base_url}{url}", timeout=5)
            status = (
                "✓ PASS"
                if response.status_code < 400
                else f"✗ FAIL ({response.status_code})"
            )
            print(f"{status:15} {name:15} {url}")
        except Exception as e:
            print(f"✗ ERROR      {name:15} {url} - {str(e)}")

    print("=" * 50)


if __name__ == "__main__":
    test_urls()
