import os
import sys
import django
from django.test import Client
from bs4 import BeautifulSoup
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

import os
import sys
import django
from django.test import Client
from django.contrib.auth import get_user_model
from bs4 import BeautifulSoup
import re

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
sys.path.insert(0, r'd:\REPOS\fleet_mgmt_django')
django.setup()

User = get_user_model()

def get_or_create_test_user():
    username = 'testuser_diag'
    password = 'testpassword123'
    email = 'test_diag@example.com'
    try:
        user = User.objects.get(username=username)
        user.set_password(password)
        user.save()
    except User.DoesNotExist:
        user = User.objects.create_user(username=username, email=email, password=password)
    return user, password

def diagnose_page(client, url, name):
    print(f"\nFetching {name} ({url}) ...")
    response = client.get(url)
    
    if response.status_code != 200:
        print(f"❌ Error: Status code {response.status_code}")
        return []

    html = response.content.decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')
    
    # Remove scripts and styles
    for script in soup(["script", "style"]):
        script.decompose()
        
    # Get text
    text = soup.get_text(separator='\n')
    
    # Clean up text
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    potential_untranslated = []
    
    # Heuristic: English words/sentences that are likely untranslated
    # We filter out common things like numbers, short codes, etc.
    # And we check if they appear in the French output.
    
    ignore_list = ['EN', 'DE', 'FR', 'ES', 'PL', '© 2025', 'testuser_diag']
    
    for line in lines:
        if line in ignore_list:
            continue
            
        # Heuristic: if it contains typical English words
        if re.search(r'\b(Home|Login|Register|Logout|Vehicle|Maintenance|Emergency|Admin|Welcome|Manage|System|Overview|Online|Quick|Actions|Report|Schedule|Recent|Activity|Premium|Solution)\b', line, re.IGNORECASE):
             potential_untranslated.append(line)
             
    if potential_untranslated:
        print(f"⚠️  Potential untranslated strings in {name}:")
        for item in set(potential_untranslated):
            print(f"   - {item}")
    else:
        print(f"✅ {name} looks good!")
        
    return potential_untranslated

def diagnose_all_pages():
    client = Client()
    
    # 1. Public Pages
    diagnose_page(client, '/fr/', 'Home Page (Public)')
    diagnose_page(client, '/fr/accounts/login/', 'Login Page')
    diagnose_page(client, '/fr/accounts/register/', 'Register Page')
    
    # 2. Authenticated Pages
    user, password = get_or_create_test_user()
    login_success = client.login(username=user.username, password=password)
    if login_success:
        print("\n✅ Logged in successfully")
        diagnose_page(client, '/fr/', 'Home Page (Authenticated)')
        diagnose_page(client, '/fr/vehicles/', 'Vehicle List')
        diagnose_page(client, '/fr/maintenance/', 'Maintenance List')
        diagnose_page(client, '/fr/emergency/', 'Emergency List')
    else:
        print("\n❌ Login failed")

if __name__ == "__main__":
    diagnose_all_pages()
