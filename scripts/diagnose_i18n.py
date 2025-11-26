#!/usr/bin/env python
"""
Diagnostic script to test Django i18n system
Generates detailed logs about template rendering and translation loading
"""
import os
import sys
import django
import logging

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(levelname)s - %(name)s - %(message)s'
)

from django.conf import settings
from django.template import engines, Context, Template
from django.utils.translation import activate, get_language
from django.test import RequestFactory
from CarFleetManagement.urls import root_view

print("="*80)
print("DJANGO I18N DIAGNOSTIC TEST")
print("="*80)

# Test 1: Settings
print("\n1. SETTINGS CHECK")
print(f"   USE_I18N: {settings.USE_I18N}")
print(f"   LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
print(f"   LANGUAGES: {settings.LANGUAGES}")
print(f"   LocaleMiddleware in MIDDLEWARE: {'django.middleware.locale.LocaleMiddleware' in settings.MIDDLEWARE}")

# Test 2: Template Engine
print("\n2. TEMPLATE ENGINE CHECK")
engine = engines['django']
print(f"   Engine: {engine}")
print(f"   Builtins: {engine.engine.builtins}")
print(f"   i18n in builtins: {'django.templatetags.i18n' in engine.engine.builtins}")

# Test 3: Direct Template Test
print("\n3. DIRECT TEMPLATE TEST")
activate('fr')
print(f"   Current language: {get_language()}")

test_template = Template("{% load i18n %}{% trans 'Home' %}")
rendered = test_template.render(Context({}))
print(f"   Template: {test_template.source}")
print(f"   Rendered: '{rendered}'")
if rendered == "Home":
    print("   ❌ FAIL: Translation not working (still shows 'Home')")
elif "{% trans" in rendered:
    print("   ❌ FAIL: Template tag not processed (shows raw tag)")
else:
    print(f"   ✅ PASS: Got translation: '{rendered}'")

# Test 4: Check .mo files
print("\n4. TRANSLATION FILES CHECK")
for lang_code, lang_name in settings.LANGUAGES:
    mo_file = settings.BASE_DIR / f"locale/{lang_code}/LC_MESSAGES/django.mo"
    po_file = settings.BASE_DIR / f"locale/{lang_code}/LC_MESSAGES/django.po"
    print(f"   {lang_code} ({lang_name}):")
    print(f"      .po exists: {po_file.exists()}")
    print(f"      .mo exists: {mo_file.exists()}")
    if mo_file.exists():
        print(f"      .mo size: {mo_file.stat().st_size} bytes")

# Test 5: Test actual view rendering
print("\n5. VIEW RENDERING TEST")
rf = RequestFactory()
request = rf.get('/fr/')
request.LANGUAGE_CODE = 'fr'

try:
    from django.contrib.auth.models import AnonymousUser
    request.user = AnonymousUser()
    response = root_view(request)
    content = response.content.decode('utf-8')
    
    print(f"   Status: {response.status_code}")
    if '{% trans' in content:
        print("   ❌ FAIL: Raw template tags in response")
        # Find first occurrence
        idx = content.find('{% trans')
        print(f"   First tag at position {idx}:")
        print(f"   Context: ...{content[max(0, idx-30):idx+80]}...")
    else:
        print("   ✅ PASS: No raw template tags")
        
    if 'Accueil' in content or 'Connexion' in content:
        print("   ✅ PASS: French translations found")
    else:
        print("   ❌ FAIL: No French translations found")
        
except Exception as e:
    print(f"   ❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 6: Check if i18n is loaded in base_v2.html
print("\n6. BASE TEMPLATE CHECK")
base_template_path = settings.BASE_DIR / "CarFleetManagement/templates/base_v2.html"
if base_template_path.exists():
    with open(base_template_path, 'r', encoding='utf-8') as f:
        content = f.read()
        has_load_i18n = '{% load i18n %}' in content
        has_load_static = '{% load static %}' in content
        print(f"   File exists: ✅")
        print(f"   Has {{% load i18n %}}: {'✅' if has_load_i18n else '❌'}")
        print(f"   Has {{% load static %}}: {'✅' if has_load_static else '❌'}")
        print(f"   First 200 chars: {content[:200]}")
else:
    print(f"   ❌ File not found: {base_template_path}")

print("\n" + "="*80)
print("DIAGNOSTIC COMPLETE")
print("="*80)
