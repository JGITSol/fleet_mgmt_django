#!/usr/bin/env python3
"""
Test Django URL resolution
"""

import os
import sys
from pathlib import Path

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')

import django
django.setup()

from django.urls import get_resolver, reverse, NoReverseMatch
from django.test import Client

def test_url_resolution():
    """Test URL resolution"""
    print("Testing Django URL Resolution")
    print("=" * 50)
    
    # Get the URL resolver
    resolver = get_resolver()
    
    # Print all URL patterns
    print("Available URL patterns:")
    for pattern in resolver.url_patterns:
        print(f"  {pattern}")
    
    print("\n" + "=" * 50)
    
    # Test specific URLs
    test_urls = [
        '/',
        '/admin/',
        '/api/',
        '/accounts/login/',
        '/vehicles/',
        '/maintenance/',
        '/emergency/',
    ]
    
    client = Client()
    
    print("Testing URL accessibility:")
    for url in test_urls:
        try:
            response = client.get(url)
            status = "✓ PASS" if response.status_code < 400 else f"✗ FAIL ({response.status_code})"
            print(f"  {status:15} {url}")
        except Exception as e:
            print(f"  ✗ ERROR      {url} - {str(e)}")

if __name__ == "__main__":
    test_url_resolution()