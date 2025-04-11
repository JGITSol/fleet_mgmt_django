from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from accounts.models import UserRole, Driver, EmergencyContact
from vehicles.models import Vehicle
from maintenance.models import Maintenance
from emergency.models import EmergencyIncident
from django.utils import timezone
from datetime import timedelta

User = get_user_model()

class AccountViewsTestCase(TestCase):
    """Test cases for the accounts app views."""
    
    def setUp(self):
        """Set up test environment."""
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.FLEET_MANAGER, description='Fleet Manager role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role
        )
        
        self.fleet_manager_user = User.objects.create_user(
            username='fleet_manager',
            email='fleet@example.com',
            password='password123',
            role=self.fleet_manager_role
        )
        
        self.driver_user = User.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        self.maintenance_user = User.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )
        
        self.no_role_user = User.objects.create_user(
            username='no_role_user',
            email='norole@example.com',
            password='password123',
            role=None
        )
        
        # Create client
        self.client = Client()
    
    def test_signup_view_get(self):
        """Test signup view GET request."""
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')
    
    def test_signup_view_post(self):
        """Test signup view POST request."""
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'password1': 'testpassword123',
            'password2': 'testpassword123'
        })
        self.assertEqual(response.status_code, 302)  # Redirect after successful signup
        self.assertTrue(User.objects.filter(username='newuser').exists())
    
    def test_dashboard_redirect_admin(self):
        """Test dashboard redirect for admin user."""
        self.client.login(username='admin_user', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('admin_dashboard'))
    
    def test_dashboard_redirect_fleet_manager(self):
        """Test dashboard redirect for fleet manager user."""
        self.client.login(username='fleet_manager', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('fleet_manager_dashboard'))
    
    def test_dashboard_redirect_driver(self):
        """Test dashboard redirect for driver user."""
        self.client.login(username='driver_user', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('driver_dashboard'))
    
    def test_dashboard_redirect_maintenance(self):
        """Test dashboard redirect for maintenance user."""
        self.client.login(username='maintenance_user', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('technician_dashboard'))
    
    def test_dashboard_redirect_no_role(self):
        """Test dashboard redirect for user with no role."""
        self.client.login(username='no_role_user', password='password123')
        response = self.client.get(reverse('dashboard'))
        self.assertRedirects(response, reverse('home'))
    
    def test_admin_dashboard_access(self):
        """Test admin dashboard access."""
        # Admin user should have access
        self.client.login(username='admin_user', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Non-admin user should be redirected
        self.client.login(username='driver_user', password='password123')
        response = self.client.get(reverse('admin_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect
    
    def test_fleet_manager_dashboard_access(self):
        """Test fleet manager dashboard access."""
        # Fleet manager should have access
        self.client.login(username='fleet_manager', password='password123')
        response = self.client.get(reverse('fleet_manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Admin should also have access
        self.client.login(username='admin_user', password='password123')
        response = self.client.get(reverse('fleet_manager_dashboard'))
        self.assertEqual(response.status_code, 200)
        
        # Driver should not have access
        self.client.login(username='driver_user', password='password123')
        response = self.client.get(reverse('fleet_manager_dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirect