#!/usr/bin/env python3
"""
Fix migration history inconsistency
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

from django.db import connection
from django.db.migrations.recorder import MigrationRecorder

def fix_migration_history():
    """Fix the migration history inconsistency"""
    print("🔧 Fixing Migration History")
    print("=" * 50)
    
    recorder = MigrationRecorder(connection)
    
    # Get current migration records
    print("Current migration records:")
    applied_migrations = recorder.applied_migrations()
    for app, migration in applied_migrations:
        print(f"  {app}.{migration}")
    
    print("\n" + "=" * 50)
    
    # Remove the problematic emergency migration record
    print("Removing emergency.0001_initial from migration history...")
    try:
        with connection.cursor() as cursor:
            cursor.execute(
                "DELETE FROM django_migrations WHERE app = 'emergency' AND name = '0001_initial'"
            )
        print("✓ Removed emergency.0001_initial from migration history")
    except Exception as e:
        print(f"✗ Error removing migration record: {e}")
        return False
    
    # Now try to apply accounts migrations first
    print("\nAttempting to apply accounts migrations...")
    try:
        from django.core.management import execute_from_command_line
        execute_from_command_line(['manage.py', 'migrate', 'accounts'])
        print("✓ Applied accounts migrations")
    except Exception as e:
        print(f"⚠ Accounts migration issue: {e}")
    
    # Then apply emergency migrations
    print("\nAttempting to apply emergency migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate', 'emergency'])
        print("✓ Applied emergency migrations")
    except Exception as e:
        print(f"⚠ Emergency migration issue: {e}")
    
    # Apply all remaining migrations
    print("\nApplying all remaining migrations...")
    try:
        execute_from_command_line(['manage.py', 'migrate'])
        print("✓ Applied all migrations")
        return True
    except Exception as e:
        print(f"⚠ Migration issue: {e}")
        return False

if __name__ == "__main__":
    success = fix_migration_history()
    if success:
        print("\n🎉 Migration history fixed successfully!")
    else:
        print("\n⚠️ Some issues remain. Manual intervention may be needed.")