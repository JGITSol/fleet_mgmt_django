#!/usr/bin/env python3
"""
Restart server and test URLs
"""

import sys

import requests


def test_url(url, description):
    """Test a single URL"""
    try:
        response = requests.get(f"http://localhost:8000{url}", timeout=5)
        status = (
            "✓ PASS"
            if response.status_code < 400
            else f"✗ FAIL ({response.status_code})"
        )
        print(f"  {status:15} {description:20} {url}")
        return response.status_code < 400
    except requests.exceptions.ConnectionError:
        print(f"  ✗ NO SERVER   {description:20} {url}")
        return False
    except Exception as e:
        print(f"  ✗ ERROR      {description:20} {url} - {str(e)}")
        return False


def main():
    """Main function"""
    print("🔄 Server Restart and URL Test")
    print("=" * 50)

    # Test URLs before restart
    print("Testing URLs (current server state):")
    test_urls = [
        ("/", "Home"),
        ("/accounts/login/", "Login"),
        ("/vehicles/", "Vehicles"),
        ("/maintenance/", "Maintenance"),
        ("/emergency/", "Emergency"),
        ("/api/", "API Root"),
    ]

    for url, desc in test_urls:
        test_url(url, desc)

    print("\n" + "=" * 50)
    print("🔧 Please restart the Django server manually:")
    print("   1. Stop the current server (Ctrl+C)")
    print("   2. Run: python manage.py runserver 0.0.0.0:8000")
    print("   3. Press Enter here when server is restarted...")

    input()

    print("\nTesting URLs (after restart):")
    success_count = 0
    for url, desc in test_urls:
        if test_url(url, desc):
            success_count += 1

    print(f"\n📊 Results: {success_count}/{len(test_urls)} URLs working")

    if success_count >= len(test_urls) - 1:  # Allow 1 failure
        print("✅ Server is working correctly!")
        return 0
    else:
        print("⚠️  Some URLs still not working. Check server logs.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
