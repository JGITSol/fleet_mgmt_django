#!/usr/bin/env python
"""Diagnose why templates are rendering as literal text"""
import os
import sys
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

from django.test import RequestFactory
from django.contrib.auth.models import AnonymousUser
from CarFleetManagement.urls import root_view
from django.template import engines
from django.conf import settings

print("="*60)
print("TEMPLATE ENGINE DIAGNOSIS")
print("="*60)

# Check template engines
print("\n1. Template Engines Configured:")
for engine in engines.all():
    print(f"   - {engine.name}: {engine.__class__.__name__}")

# Check template directories
print("\n2. Template Directories:")
for config in settings.TEMPLATES:
    print(f"   Backend: {config['BACKEND']}")
    print(f"   DIRS: {config.get('DIRS', [])}")
    print(f"   APP_DIRS: {config.get('APP_DIRS', False)}")

# Test rendering
print("\n3. Testing Template Rendering:")
try:
    rf = RequestFactory()
    request = rf.get('/')
    request.user = AnonymousUser()
    
    response = root_view(request)
    content = response.content.decode('utf-8')
    
    print(f"   Status Code: {response.status_code}")
    print(f"   Content-Type: {response.get('Content-Type', 'Not set')}")
    
    # Check for raw template tags
    if '{% trans' in content:
        print("   ❌ RAW TEMPLATE TAGS FOUND IN OUTPUT!")
        print(f"   First occurrence: {content.find('{% trans')}")
        
        # Show context around first occurrence
        idx = content.find('{% trans')
        print(f"\n   Context (50 chars before and after):")
        print(f"   ...{content[max(0, idx-50):idx+100]}...")
    else:
        print("   ✅ No raw template tags found")
        
    # Check if it's HTML
    if '<html' in content.lower():
        print("   ✅ HTML structure detected")
    else:
        print("   ❌ No HTML structure found")
        
except Exception as e:
    print(f"   ❌ Error: {e}")
    import traceback
    traceback.print_exc()

# Check if home.html exists and is valid
print("\n4. Checking home.html:")
home_template_path = r'd:\REPOS\fleet_mgmt_django\CarFleetManagement\templates\home.html'
if os.path.exists(home_template_path):
    print(f"   ✅ File exists: {home_template_path}")
    with open(home_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        print(f"   File size: {len(content)} bytes")
        print(f"   First line: {content.split(chr(10))[0]}")
        
        # Check for template tags
        if '{% extends' in content:
            print(f"   ✅ Has {% extends %} tag")
        else:
            print(f"   ❌ Missing {% extends %} tag")
            
        if '{% load i18n %}' in content:
            print(f"   ✅ Has {% load i18n %} tag")
        else:
            print(f"   ❌ Missing {% load i18n %} tag")
else:
    print(f"   ❌ File not found: {home_template_path}")

print("\n" + "="*60)
