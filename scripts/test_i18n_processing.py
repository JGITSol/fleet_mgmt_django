import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
django.setup()

from django.template import Template, Context
from django.template.loader import get_template

# Test 1: Simple template with trans tag
print("=" * 60)
print("TEST 1: Simple template with {% trans %} tag")
print("=" * 60)

simple_template = """
{% load i18n %}
<p>{% trans "Hello World" %}</p>
"""

try:
    t = Template(simple_template)
    output = t.render(Context({}))
    print(f"Output: {output}")
    if '{% trans' in output:
        print("❌ FAILED: Template tags not processed")
    else:
        print("✅ SUCCESS: Template processed correctly")
except Exception as e:
    print(f"❌ ERROR: {e}")

# Test 2: Load base_v2.html and check
print("\n" + "=" * 60)
print("TEST 2: Loading base_v2.html template")
print("=" * 60)

try:
    template = get_template('base_v2.html')
    print(f"Template loaded from: {template.origin.name}")
    
    # Read the source
    with open(template.origin.name, 'r', encoding='utf-8') as f:
        content = f.read()
        
    # Check first few lines
    lines = content.split('\n')[:5]
    print("\nFirst 5 lines of template:")
    for i, line in enumerate(lines, 1):
        print(f"{i}: {line}")
        
    # Check if {% load i18n %} is present
    if '{% load i18n %}' in content:
        print("\n✅ Template has {% load i18n %} tag")
    else:
        print("\n❌ Template MISSING {% load i18n %} tag")
        
except Exception as e:
    print(f"❌ ERROR: {e}")
    import traceback
    traceback.print_exc()

# Test 3: Check settings
print("\n" + "=" * 60)
print("TEST 3: Check Django settings")
print("=" * 60)

from django.conf import settings

print(f"USE_I18N: {settings.USE_I18N}")
print(f"LANGUAGE_CODE: {settings.LANGUAGE_CODE}")
print(f"LANGUAGES: {settings.LANGUAGES}")

# Check template builtins
templates_config = settings.TEMPLATES[0]
print(f"\nTemplate backend: {templates_config['BACKEND']}")
print(f"APP_DIRS: {templates_config['APP_DIRS']}")
print(f"Builtins: {templates_config['OPTIONS'].get('builtins', [])}")
