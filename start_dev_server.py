#!/usr/bin/env python
"""
Development Server Startup Script
=================================

This script sets up and starts the Django development server with test credentials.
"""

import os
import sys
import subprocess
from pathlib import Path

def main():
    """Start the development server with proper setup."""
    
    print("🚀 Starting Django Car Fleet Management System (Development Mode)")
    print("=" * 60)
    
    # Change to CarFleetManagement directory
    os.chdir(Path(__file__).parent / 'CarFleetManagement')
    
    try:
        # Run migrations
        print("📦 Running database migrations...")
        result = subprocess.run([sys.executable, 'manage.py', 'migrate'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ Migration failed: {result.stderr}")
            return False
        print("✅ Migrations completed")
        
        # Set up development users
        print("👥 Setting up development test users...")
        result = subprocess.run([sys.executable, 'manage.py', 'setup_dev_users'], 
                              capture_output=True, text=True)
        if result.returncode != 0:
            print(f"❌ User setup failed: {result.stderr}")
            return False
        
        # Print the output from setup_dev_users
        print(result.stdout)
        
        # Start the development server
        print("🌐 Starting development server...")
        print("   Server will be available at: http://localhost:8000/")
        print("   Press Ctrl+C to stop the server")
        print("=" * 60)
        
        # Run the server (this will block until Ctrl+C)
        subprocess.run([sys.executable, 'manage.py', 'runserver'])
        
    except KeyboardInterrupt:
        print("\n👋 Development server stopped.")
        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)