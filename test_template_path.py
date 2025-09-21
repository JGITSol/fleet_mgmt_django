#!/usr/bin/env python3
"""
Test template path resolution
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

from django.conf import settings
from django.template.loader import get_template

def test_template_paths():
    """Test template path resolution"""
    print("Testing Template Path Resolution")
    print("=" * 50)
    
    print(f"BASE_DIR: {settings.BASE_DIR}")
    print(f"TEMPLATES DIRS: {settings.TEMPLATES[0]['DIRS']}")
    
    # Check if template directories exist
    for template_dir in settings.TEMPLATES[0]['DIRS']:
        print(f"Template dir exists: {template_dir} -> {template_dir.exists()}")
        if template_dir.exists():
            print(f"  Contents: {list(template_dir.iterdir())}")
    
    # Try to load the login template
    try:
        template = get_template('registration/login.html')
        print("✓ Successfully loaded registration/login.html")
    except Exception as e:
        print(f"✗ Failed to load registration/login.html: {e}")
    
    # Check if base template exists
    try:
        template = get_template('base.html')
        print("✓ Successfully loaded base.html")
    except Exception as e:
        print(f"✗ Failed to load base.html: {e}")

if __name__ == "__main__":
    test_template_paths()