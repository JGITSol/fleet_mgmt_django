#!/usr/bin/env python3
"""
Fix database schema to match current models
"""

import os
import sqlite3
import sys
from pathlib import Path

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")

import django

django.setup()


def fix_database_schema():
    """Fix database schema issues"""
    print("🔧 Fixing Database Schema")
    print("=" * 50)

    db_path = Path("CarFleetManagement/db.sqlite3")

    if not db_path.exists():
        print("✗ Database file not found")
        return False

    try:
        # Connect directly to SQLite
        conn = sqlite3.connect(str(db_path))
        cursor = conn.cursor()

        # Check current schema for accounts_customuser
        cursor.execute("PRAGMA table_info(accounts_customuser)")
        columns = cursor.fetchall()

        print("Current accounts_customuser columns:")
        for col in columns:
            print(f"  {col[1]} {col[2]} {'NOT NULL' if col[3] else 'NULL'}")

        # Make phone_number nullable if it exists and is NOT NULL
        phone_number_exists = any(col[1] == "phone_number" for col in columns)

        if phone_number_exists:
            print("\nMaking phone_number nullable...")

            # Drop the new table if it exists
            cursor.execute("DROP TABLE IF EXISTS accounts_customuser_new")

            # Create a new table with correct schema
            cursor.execute("""
                CREATE TABLE accounts_customuser_new (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    password VARCHAR(128) NOT NULL,
                    last_login DATETIME,
                    is_superuser BOOLEAN NOT NULL,
                    username VARCHAR(150) NOT NULL UNIQUE,
                    first_name VARCHAR(150) NOT NULL,
                    last_name VARCHAR(150) NOT NULL,
                    email VARCHAR(254) NOT NULL,
                    is_staff BOOLEAN NOT NULL,
                    is_active BOOLEAN NOT NULL,
                    date_joined DATETIME NOT NULL,
                    role_id INTEGER,
                    phone_number VARCHAR(20),
                    emergency_contact VARCHAR(100),
                    FOREIGN KEY (role_id) REFERENCES accounts_userrole (id)
                )
            """)

            # Copy data from old table (only columns that exist)
            cursor.execute("""
                INSERT INTO accounts_customuser_new 
                SELECT id, password, last_login, is_superuser, username, first_name, last_name, 
                       email, is_staff, is_active, date_joined, role_id, 
                       COALESCE(phone_number, '') as phone_number,
                       '' as emergency_contact
                FROM accounts_customuser
            """)

            # Drop old table and rename new one
            cursor.execute("DROP TABLE accounts_customuser")
            cursor.execute(
                "ALTER TABLE accounts_customuser_new RENAME TO accounts_customuser"
            )

            print("✓ Fixed phone_number column to be nullable")

        # Check if permissions column exists in accounts_userrole
        cursor.execute("PRAGMA table_info(accounts_userrole)")
        role_columns = cursor.fetchall()

        print("\nCurrent accounts_userrole columns:")
        for col in role_columns:
            print(f"  {col[1]} {col[2]}")

        permissions_exists = any(col[1] == "permissions" for col in role_columns)

        if not permissions_exists:
            print("\nAdding permissions column to accounts_userrole...")
            cursor.execute(
                "ALTER TABLE accounts_userrole ADD COLUMN permissions TEXT DEFAULT '{}'"
            )
            print("✓ Added permissions column")

        conn.commit()
        conn.close()

        print("\n✓ Database schema fixed successfully")
        return True

    except Exception as e:
        print(f"✗ Error fixing database schema: {e}")
        return False


if __name__ == "__main__":
    fix_database_schema()
