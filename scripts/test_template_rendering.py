import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
django.setup()

from django.template.loader import render_to_string
from django.test import RequestFactory

# Create a test request
rf = RequestFactory()
request = rf.get('/')

# Try to render the home template
try:
    output = render_to_string('home.html', request=request)
    
    # Check if template tags are being processed
    if '{% trans' in output or '{%' in output:
        print("❌ PROBLEM FOUND: Template tags are NOT being processed!")
        print("\nRaw template tags found in output:")
        # Show first occurrence
        idx = output.find('{%')
        if idx != -1:
            print(output[max(0, idx-50):idx+100])
    else:
        print("✅ Template rendering works correctly")
        print("\nFirst 500 characters of rendered output:")
        print(output[:500])
        
except Exception as e:
    print(f"❌ ERROR rendering template: {e}")
    import traceback
    traceback.print_exc()
