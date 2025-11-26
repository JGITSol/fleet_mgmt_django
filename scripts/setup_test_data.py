import os
import sys
import django
from django.utils import timezone
from datetime import timedelta

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'CarFleetManagement.settings')
django.setup()

from CarFleetManagement.accounts.models import CustomUser, UserRole, Driver
from CarFleetManagement.vehicles.models import Vehicle
from CarFleetManagement.maintenance.models import Maintenance, MaintenanceType, MaintenanceStatus

def create_roles():
    print("Creating roles...")
    roles = [
        (UserRole.ADMIN, 'Administrator'),
        (UserRole.MANAGER, 'Fleet Manager'),
        (UserRole.COORDINATOR, 'Coordinator'),
        (UserRole.DRIVER, 'Driver'),
        (UserRole.TESTUSER, 'Test User'),
        (UserRole.MAINTENANCE_STAFF, 'Maintenance Staff'),
    ]
    for code, name in roles:
        UserRole.objects.get_or_create(name=code, defaults={'description': name})

def create_users():
    print("Creating users...")
    admin_role = UserRole.objects.get(name=UserRole.ADMIN)
    
    if not CustomUser.objects.filter(username='admin').exists():
        CustomUser.objects.create_superuser('admin', 'admin@example.com', 'adminpassword', role=admin_role)
        print("Created superuser: admin/adminpassword")
    
    if not CustomUser.objects.filter(username='testuser').exists():
        CustomUser.objects.create_user('testuser', 'test@example.com', 'password123', role=admin_role)
        print("Created test user: testuser/password123")

def create_vehicles():
    print("Creating vehicles...")
    vehicles_data = [
        {
            'brand': 'Ford', 'model': 'F-150', 'year': 2022, 
            'license_plate': 'ABC-123', 'vin': '1FTEW1CP5KFA12345',
            'vehicle_type': Vehicle.VehicleType.TRUCK,
            'status': Vehicle.Status.AVAILABLE
        },
        {
            'brand': 'Toyota', 'model': 'Camry', 'year': 2021, 
            'license_plate': 'XYZ-789', 'vin': '4T1B11HK4MU123456',
            'vehicle_type': Vehicle.VehicleType.SUV, # Just using SUV for simplicity
            'status': Vehicle.Status.IN_USE
        },
        {
            'brand': 'Mercedes', 'model': 'Sprinter', 'year': 2020, 
            'license_plate': 'VAN-456', 'vin': 'WD3PE7CC9K5123456',
            'vehicle_type': Vehicle.VehicleType.VAN,
            'status': Vehicle.Status.MAINTENANCE
        }
    ]
    
    for v_data in vehicles_data:
        Vehicle.objects.get_or_create(license_plate=v_data['license_plate'], defaults=v_data)

def create_maintenance():
    print("Creating maintenance records...")
    vehicle = Vehicle.objects.filter(license_plate='VAN-456').first()
    if vehicle:
        Maintenance.objects.get_or_create(
            vehicle=vehicle,
            scheduled_date=timezone.now().date(),
            defaults={
                'maintenance_type': MaintenanceType.ROUTINE,
                'status': MaintenanceStatus.IN_PROGRESS,
                'description': 'Regular oil change and tire rotation',
                'odometer_reading': 50000,
                'cost': 150.00,
                'service_provider': 'QuickFix Auto'
            }
        )

if __name__ == '__main__':
    create_roles()
    create_users()
    create_vehicles()
    create_maintenance()
    print("Setup complete!")
