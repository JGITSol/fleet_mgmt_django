import os
import sys
import django
from django.utils.translation import activate, gettext

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

def debug_translation():
    lang = 'fr'
    activate(lang)
    
    print(f"Activated language: {lang}")
    
    keys_to_test = [
        "Welcome to Fleet Management",
        "Home",
        "FleetManager"
    ]
    
    for key in keys_to_test:
        trans = gettext(key)
        print(f"Original: '{key}'")
        print(f"Translated: '{trans}'")
        if trans == key:
            print("❌ Not translated")
        else:
            print("✅ Translated")
            
if __name__ == "__main__":
    debug_translation()
