#!/usr/bin/env python3
"""
Debug URL patterns and test server responses
"""

import os
import sys
from pathlib import Path

import requests

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

import django

django.setup()

from django.test import Client
from django.urls import get_resolver


def debug_url_patterns():
    """Debug URL patterns in detail"""
    print("🔍 Debugging URL Patterns")
    print("=" * 50)

    resolver = get_resolver()

    print("Root URL patterns:")
    for i, pattern in enumerate(resolver.url_patterns):
        print(f"  {i + 1}. {pattern}")

        # If it's a URLResolver (includes other URLs), show its patterns too
        if hasattr(pattern, "url_patterns"):
            print(f"     Namespace: {getattr(pattern, 'namespace', 'None')}")
            print(f"     App name: {getattr(pattern, 'app_name', 'None')}")
            for j, sub_pattern in enumerate(pattern.url_patterns):
                print(f"       {i + 1}.{j + 1} {sub_pattern}")

    print("\n" + "=" * 50)

    # Test specific URL resolution
    test_urls = [
        "/accounts/login/",
        "/vehicles/",
        "/maintenance/",
        "/emergency/",
    ]

    print("Testing URL resolution:")
    client = Client()

    for url in test_urls:
        try:
            response = client.get(url)
            print(f"  {url:20} -> {response.status_code} (Django client)")
        except Exception as e:
            print(f"  {url:20} -> ERROR: {e}")

    print("\nTesting external HTTP requests:")
    for url in test_urls:
        try:
            response = requests.get(f"http://localhost:8000{url}", timeout=5)
            print(f"  {url:20} -> {response.status_code} (HTTP request)")
        except Exception as e:
            print(f"  {url:20} -> ERROR: {e}")


if __name__ == "__main__":
    debug_url_patterns()
