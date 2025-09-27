#!/usr/bin/env python3
"""
Test JWT authentication
"""

import requests
import json

def test_jwt_authentication():
    """Test JWT authentication flow"""
    print("🔐 Testing JWT Authentication")
    print("=" * 50)
    
    base_url = "http://localhost:8000"
    
    # Test login
    login_data = {
        'username': 'testuser',
        'password': 'testpass123'
    }
    
    print("Testing login...")
    try:
        response = requests.post(f"{base_url}/api/auth/login/", json=login_data)
        print(f"Login response status: {response.status_code}")
        print(f"Login response: {response.text[:200]}")
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            
            if access_token:
                print("✓ JWT token obtained successfully")
                
                # Test authenticated API call
                headers = {'Authorization': f'Bearer {access_token}'}
                
                print("\nTesting authenticated API calls...")
                
                # Test vehicles API
                vehicles_response = requests.get(f"{base_url}/api/vehicles/", headers=headers)
                print(f"Vehicles API: {vehicles_response.status_code}")
                
                # Test drivers API
                drivers_response = requests.get(f"{base_url}/api/drivers/", headers=headers)
                print(f"Drivers API: {drivers_response.status_code}")
                
                # Test maintenance API
                maintenance_response = requests.get(f"{base_url}/api/maintenance/", headers=headers)
                print(f"Maintenance API: {maintenance_response.status_code}")
                
                # Test emergencies API
                emergencies_response = requests.get(f"{base_url}/api/emergencies/", headers=headers)
                print(f"Emergencies API: {emergencies_response.status_code}")
                
                if all(r.status_code < 400 for r in [vehicles_response, drivers_response, maintenance_response, emergencies_response]):
                    print("✓ All API endpoints working with JWT authentication")
                    return True
                else:
                    print("✗ Some API endpoints still failing")
                    return False
            else:
                print("✗ No access token in response")
                return False
        else:
            print(f"✗ Login failed: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"✗ Error testing JWT authentication: {e}")
        return False

if __name__ == "__main__":
    success = test_jwt_authentication()
    if success:
        print("\n🎉 JWT authentication working perfectly!")
    else:
        print("\n⚠️ JWT authentication issues remain")