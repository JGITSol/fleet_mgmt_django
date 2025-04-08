from django.test import TestCase
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils import timezone
from datetime import timedelta

from accounts.models import UserRole, Driver, EmergencyContact
from vehicles.models import Vehicle

User = get_user_model()

class UserRoleTestCase(TestCase):
    """Test cases for the UserRole model."""
    
    def setUp(self):
        """Set up test environment."""
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.FLEET_MANAGER, description='Fleet Manager role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
    
    def test_role_creation(self):
        """Test UserRole creation."""
        self.assertEqual(self.admin_role.name, UserRole.ADMIN)
        self.assertEqual(self.admin_role.description, 'Administrator role')
        self.assertEqual(str(self.admin_role), 'Administrator')
        
        self.assertEqual(self.fleet_manager_role.name, UserRole.FLEET_MANAGER)
        self.assertEqual(str(self.fleet_manager_role), 'Fleet Manager')
        
        self.assertEqual(self.driver_role.name, UserRole.DRIVER)
        self.assertEqual(str(self.driver_role), 'Driver')
        
        self.assertEqual(self.maintenance_role.name, UserRole.MAINTENANCE_STAFF)
        self.assertEqual(str(self.maintenance_role), 'Maintenance Staff')

class CustomUserTestCase(TestCase):
    """Test cases for the CustomUser model."""
    
    def setUp(self):
        """Set up test environment."""
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role,
            phone_number='123-456-7890'
        )
        
        self.driver_user = User.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role,
            phone_number='098-765-4321'
        )
    
    def test_user_creation(self):
        """Test CustomUser creation."""
        self.assertEqual(self.admin_user.username, 'admin_user')
        self.assertEqual(self.admin_user.email, 'admin@example.com')
        self.assertEqual(self.admin_user.phone_number, '123-456-7890')
        self.assertEqual(self.admin_user.role, self.admin_role)
        
        self.assertEqual(self.driver_user.username, 'driver_user')
        self.assertEqual(self.driver_user.role, self.driver_role)
    
    def test_user_role_properties(self):
        """Test CustomUser role properties."""
        self.assertTrue(self.admin_user.is_admin)
        self.assertFalse(self.admin_user.is_driver)
        self.assertFalse(self.admin_user.is_fleet_manager)
        self.assertFalse(self.admin_user.is_maintenance_staff)
        
        self.assertFalse(self.driver_user.is_admin)
        self.assertTrue(self.driver_user.is_driver)
        self.assertFalse(self.driver_user.is_fleet_manager)
        self.assertFalse(self.driver_user.is_maintenance_staff)

class DriverTestCase(TestCase):
    """Test cases for the Driver model."""
    
    def setUp(self):
        """Set up test environment."""
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER)
        
        self.user = User.objects.create_user(
            username='test_driver',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456'
        )
        
        self.driver = Driver.objects.create(
            user=self.user,
            first_name='John',
            last_name='Doe',
            email='john.doe@example.com',
            phone_number='123-456-7890',
            driver_license_number='DL12345678',
            license_expiry_date=timezone.now().date() + timedelta(days=365),
            hire_date=timezone.now().date() - timedelta(days=30)
        )
        self.driver.assigned_vehicles.add(self.vehicle)
    
    def test_driver_creation(self):
        """Test Driver creation."""
        self.assertEqual(self.driver.first_name, 'John')
        self.assertEqual(self.driver.last_name, 'Doe')
        self.assertEqual(self.driver.email, 'john.doe@example.com')
        self.assertEqual(self.driver.phone_number, '123-456-7890')
        self.assertEqual(self.driver.driver_license_number, 'DL12345678')
        self.assertEqual(self.driver.user, self.user)
    
    def test_driver_string_representation(self):
        """Test Driver string representation."""
        self.assertEqual(str(self.driver), 'John Doe')
    
    def test_driver_full_name_property(self):
        """Test Driver full_name property."""
        self.assertEqual(self.driver.full_name, 'John Doe')
    
    def test_driver_vehicle_assignment(self):
        """Test Driver vehicle assignment."""
        self.assertEqual(self.driver.assigned_vehicles.count(), 1)
        self.assertEqual(self.driver.assigned_vehicles.first(), self.vehicle)

class EmergencyContactTestCase(TestCase):
    """Test cases for the EmergencyContact model."""
    
    def setUp(self):
        """Set up test environment."""
        self.user = User.objects.create_user(
            username='test_user',
            email='user@example.com',
            password='password123'
        )
        
        self.emergency_contact = EmergencyContact.objects.create(
            user=self.user,
            name='Jane Doe',
            phone_number='123-456-7890',
            relationship='Spouse'
        )
    
    def test_emergency_contact_creation(self):
        """Test EmergencyContact creation."""
        self.assertEqual(self.emergency_contact.name, 'Jane Doe')
        self.assertEqual(self.emergency_contact.phone_number, '123-456-7890')
        self.assertEqual(self.emergency_contact.relationship, 'Spouse')
        self.assertEqual(self.emergency_contact.user, self.user)
    
    def test_emergency_contact_string_representation(self):
        """Test EmergencyContact string representation."""
        expected_str = 'Jane Doe (Spouse of test_user)'
        self.assertEqual(str(self.emergency_contact), expected_str)