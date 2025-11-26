#!/usr/bin/env python
"""
Development Server Startup Script
=================================

This script sets up and starts the Django development server with test credentials.
"""

import os
import subprocess
import sys
from pathlib import Path

# Force UTF-8 output for Windows consoles
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")


def main():
    """Start the development server with proper setup."""

    print("Starting Django Car Fleet Management System (Development Mode)")
    print("=" * 60)

    # Change to project root directory (where manage.py is)
    os.chdir(Path(__file__).parent.parent)

    try:
        # Run migrations
        print("Running database migrations...")
        migrate_cmd = [sys.executable, "manage.py", "migrate"]
        if not all(all(c.isalnum() or c in "-_./\\: " for c in a) for a in migrate_cmd):
            print(f"Refusing to run unsafe migrate command: {migrate_cmd}")
            return False
        result = subprocess.run(migrate_cmd, capture_output=True, text=True)  # noqa: S603
        if result.returncode != 0:
            print(f"Migration failed: {result.stderr}")
            return False
        print("Migrations completed")

        # Set up development users
        print("Setting up development test users...")
        setup_cmd = [sys.executable, "manage.py", "setup_dev_users"]
        if not all(all(c.isalnum() or c in "-_./\\: " for c in a) for a in setup_cmd):
            print(f"Refusing to run unsafe setup command: {setup_cmd}")
            return False
        result = subprocess.run(setup_cmd, capture_output=True, text=True, encoding='utf-8', errors='replace')  # noqa: S603
        if result.returncode != 0:
            print(f"User setup failed: {result.stderr}")
            return False

        # Print the output from setup_dev_users
        try:
            print(result.stdout)
        except UnicodeEncodeError:
            print(result.stdout.encode('ascii', 'replace').decode('ascii'))

        # Start the development server
        print("Starting development server...")
        print("   Server will be available at: http://localhost:8000/")
        print("   Press Ctrl+C to stop the server")
        print("=" * 60)

        # Run the server (this will block until Ctrl+C)
        run_cmd = [sys.executable, "manage.py", "runserver"]
        if not all(all(c.isalnum() or c in "-_./\\: " for c in a) for a in run_cmd):
            print(f"Refusing to run unsafe server command: {run_cmd}")
            return False
        subprocess.run(run_cmd)  # noqa: S603

    except KeyboardInterrupt:
        print("\n👋 Development server stopped.")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
