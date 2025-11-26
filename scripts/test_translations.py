#!/usr/bin/env python
"""
Automated Translation System Test
Tests template rendering, translation loading, and language switching
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

from django.test import RequestFactory, Client
from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.utils.translation import activate, get_language
from django.conf import settings

def test_template_rendering():
    """Test that templates render without showing raw template tags"""
    print("\n" + "="*60)
    print("TEST 1: Template Rendering")
    print("="*60)
    
    try:
        # Render home template
        html = render_to_string('home.html', {})
        
        # Check for raw template tags (should NOT appear)
        if '{% trans' in html:
            print("❌ FAIL: Raw template tags found in rendered HTML")
            print(f"   Found: {html[:200]}")
            return False
        elif '{% load' in html:
            print("❌ FAIL: Raw {% load %} tags found in rendered HTML")
            return False
        else:
            print("✅ PASS: Template rendered correctly (no raw tags)")
            print(f"   First 200 chars: {html[:200]}")
            return True
    except Exception as e:
        print(f"❌ FAIL: Template rendering error: {e}")
        return False

def test_translation_files():
    """Test that translation files exist and are compiled"""
    print("\n" + "="*60)
    print("TEST 2: Translation Files")
    print("="*60)
    
    results = []
    for lang_code in ['fr', 'pl']:
        po_file = f'd:\\REPOS\\fleet_mgmt_django\\locale\\{lang_code}\\LC_MESSAGES\\django.po'
        mo_file = f'd:\\REPOS\\fleet_mgmt_django\\locale\\{lang_code}\\LC_MESSAGES\\django.mo'
        
        po_exists = os.path.exists(po_file)
        mo_exists = os.path.exists(mo_file)
        
        print(f"\n{lang_code.upper()}:")
        print(f"  .po file: {'✅' if po_exists else '❌'} {po_file}")
        print(f"  .mo file: {'✅' if mo_exists else '❌'} {mo_file}")
        
        if po_exists and mo_exists:
            # Check if .mo is newer than .po
            po_time = os.path.getmtime(po_file)
            mo_time = os.path.getmtime(mo_file)
            if mo_time >= po_time:
                print(f"  ✅ .mo file is up to date")
                results.append(True)
            else:
                print(f"  ❌ .mo file is OUTDATED (needs recompilation)")
                results.append(False)
        else:
            results.append(False)
    
    return all(results)

def test_language_switching():
    """Test that language switching works"""
    print("\n" + "="*60)
    print("TEST 3: Language Switching")
    print("="*60)
    
    client = Client()
    results = []
    
    for lang_code, lang_name in [('en', 'English'), ('fr', 'French'), ('pl', 'Polish')]:
        print(f"\nTesting {lang_name} ({lang_code}):")
        
        # Activate language
        activate(lang_code)
        current_lang = get_language()
        
        if current_lang == lang_code:
            print(f"  ✅ Language activated: {current_lang}")
            
            # Try to render a simple translated string
            from django.utils.translation import gettext as _
            test_str = _("Home")
            print(f"  Translation of 'Home': '{test_str}'")
            
            # For non-English, check if translation is different
            if lang_code != 'en':
                if test_str != "Home":
                    print(f"  ✅ Translation working (got '{test_str}')")
                    results.append(True)
                else:
                    print(f"  ⚠️  Translation missing (still 'Home')")
                    results.append(False)
            else:
                results.append(True)
        else:
            print(f"  ❌ Language activation failed")
            results.append(False)
    
    return all(results)

def test_http_response():
    """Test actual HTTP response from the view"""
    print("\n" + "="*60)
    print("TEST 4: HTTP Response")
    print("="*60)
    
    client = Client()
    
    # Test English
    response = client.get('/')
    print(f"\nEnglish (/):")
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if '{% trans' in content:
            print(f"  ❌ Raw template tags in response!")
            print(f"  First 300 chars: {content[:300]}")
            return False
        else:
            print(f"  ✅ Clean HTML response")
            print(f"  First 200 chars: {content[:200]}")
    
    # Test French
    response = client.get('/fr/')
    print(f"\nFrench (/fr/):")
    print(f"  Status: {response.status_code}")
    
    if response.status_code == 200:
        content = response.content.decode('utf-8')
        if '{% trans' in content:
            print(f"  ❌ Raw template tags in response!")
            return False
        else:
            print(f"  ✅ Clean HTML response")
            # Check for French content
            if 'Accueil' in content or 'Connexion' in content:
                print(f"  ✅ French translations detected!")
                return True
            else:
                print(f"  ⚠️  No French translations found")
                return False
    
    return False

def main():
    print("\n" + "="*60)
    print("AUTOMATED TRANSLATION SYSTEM TEST")
    print("="*60)
    
    results = {
        'Template Rendering': test_template_rendering(),
        'Translation Files': test_translation_files(),
        'Language Switching': test_language_switching(),
        'HTTP Response': test_http_response(),
    }
    
    print("\n" + "="*60)
    print("SUMMARY")
    print("="*60)
    
    for test_name, passed in results.items():
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
    
    total = len(results)
    passed = sum(results.values())
    print(f"\nTotal: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} test(s) failed")
        return 1

if __name__ == '__main__':
    sys.exit(main())
