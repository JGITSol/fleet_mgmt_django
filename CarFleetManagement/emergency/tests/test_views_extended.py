"""
Extended tests for emergency views to improve coverage.
"""
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient

from CarFleetManagement.accounts.models import UserRole
from CarFleetManagement.emergency.models import EmergencyIncident, EmergencyResponse
from CarFleetManagement.vehicles.models import Vehicle

User = get_user_model()


class EmergencyViewsExtendedTestCase(TestCase):
    """Extended test cases for emergency views."""

    def setUp(self):
        """Set up test data."""
        # Create roles
        self.admin_role = UserRole.objects.create(name='ADMIN', description='Admin')
        self.emergency_role = UserRole.objects.create(name='EMERGENCY_STAFF', description='Emergency Staff')
        self.driver_role = UserRole.objects.create(name='DRIVER', description='Driver')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin', email='admin@test.com', password='pass', 
            role=self.admin_role, is_staff=True
        )
        self.emergency_user = User.objects.create_user(
            username='emergency', email='emergency@test.com', password='pass',
            role=self.emergency_role
        )
        self.driver_user = User.objects.create_user(
            username='driver', email='driver@test.com', password='pass',
            role=self.driver_role
        )
        
        # Create vehicle
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2020,
            license_plate='ABC-123',
            vin='1234567890',
            status='AVAILABLE'
        )
        
        # Create emergency incident
        self.incident = EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            emergency_type='ACCIDENT',
            location='Main Street',
            description='Minor accident',
            status='REPORTED',
            reported_by=self.driver_user
        )
        
        # Create emergency response
        self.response = EmergencyResponse.objects.create(
            incident=self.incident,
            responder=self.emergency_user,
            action_taken='Police dispatched',
            notes='Emergency response notes'
        )
        
        self.client = APIClient()

    def test_emergency_incident_list_view_ordering(self):
        """Test that incidents are ordered by reported_time descending."""
        # Create another incident
        incident2 = EmergencyIncident.objects.create(
            vehicle=self.vehicle,
            emergency_type='BREAKDOWN',
            location='Second Street',
            description='Engine failure',
            status='REPORTED',
            reported_by=self.driver_user
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('emergency_list'))
        
        self.assertEqual(response.status_code, 200)
        incidents = response.context['incidents']
        
        # Should be ordered by reported_time descending (newest first)
        self.assertEqual(incidents[0], incident2)
        self.assertEqual(incidents[1], self.incident)

    def test_emergency_incident_detail_view_context(self):
        """Test that detail view includes responses in context."""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('emergency_detail', kwargs={'pk': self.incident.pk}))
        
        self.assertEqual(response.status_code, 200)
        self.assertIn('responses', response.context)
        self.assertEqual(list(response.context['responses']), [self.response])

    def test_emergency_incident_create_view_form_queryset(self):
        """Test that create view shows all vehicles in form."""
        # Create another vehicle
        vehicle2 = Vehicle.objects.create(
            brand='Honda',
            model='Civic',
            year=2021,
            license_plate='XYZ-789',
            vin='0987654321',
            status='IN_USE'
        )
        
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(reverse('emergency_create'))
        
        self.assertEqual(response.status_code, 200)
        form = response.context['form']
        vehicle_queryset = form.fields['vehicle'].queryset
        
        self.assertIn(self.vehicle, vehicle_queryset)
        self.assertIn(vehicle2, vehicle_queryset)

    def test_emergency_incident_create_view_sets_reported_by(self):
        """Test that create view sets reported_by to current user."""
        self.client.force_authenticate(user=self.driver_user)
        
        data = {
            'vehicle': self.vehicle.id,
            'emergency_type': 'BREAKDOWN',
            'location': 'Test Location',
            'description': 'Test Description',
            'status': 'REPORTED',
            'reported_by': self.admin_user.id  # This should be overridden
        }
        
        response = self.client.post(reverse('emergency_create'), data)
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Check that incident was created with correct reported_by
        incident = EmergencyIncident.objects.get(description='Test Description')
        self.assertEqual(incident.reported_by, self.driver_user)

    def test_emergency_incident_create_view_success_message(self):
        """Test that create view shows success message."""
        self.client.force_authenticate(user=self.driver_user)
        
        data = {
            'vehicle': self.vehicle.id,
            'emergency_type': 'BREAKDOWN',
            'location': 'Test Location',
            'description': 'Test Description',
            'status': 'REPORTED'
        }
        
        response = self.client.post(reverse('emergency_create'), data, follow=True)
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('successfully' in str(message) for message in messages))

    def test_emergency_incident_update_view_permission_admin(self):
        """Test that admin can update incidents."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'vehicle': self.vehicle.id,
            'emergency_type': 'ACCIDENT',
            'location': 'Updated Location',
            'description': 'Updated Description',
            'status': 'IN_PROGRESS',
            'reported_by': self.driver_user.id
        }
        
        response = self.client.post(
            reverse('emergency_update', kwargs={'pk': self.incident.pk}), 
            data
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Check that incident was updated
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.location, 'Updated Location')
        self.assertEqual(self.incident.description, 'Updated Description')

    def test_emergency_incident_update_view_permission_emergency_staff(self):
        """Test that emergency staff can update incidents."""
        self.client.force_authenticate(user=self.emergency_user)
        
        data = {
            'vehicle': self.vehicle.id,
            'emergency_type': 'ACCIDENT',
            'location': 'Updated by Emergency Staff',
            'description': 'Updated Description',
            'status': 'IN_PROGRESS',
            'reported_by': self.driver_user.id
        }
        
        response = self.client.post(
            reverse('emergency_update', kwargs={'pk': self.incident.pk}), 
            data
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Check that incident was updated
        self.incident.refresh_from_db()
        self.assertEqual(self.incident.location, 'Updated by Emergency Staff')

    def test_emergency_incident_update_view_permission_denied(self):
        """Test that regular users cannot update incidents."""
        self.client.force_authenticate(user=self.driver_user)
        
        response = self.client.get(
            reverse('emergency_update', kwargs={'pk': self.incident.pk})
        )
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_emergency_incident_update_view_success_message(self):
        """Test that update view shows success message."""
        self.client.force_authenticate(user=self.admin_user)
        
        data = {
            'vehicle': self.vehicle.id,
            'emergency_type': 'ACCIDENT',
            'location': 'Updated Location',
            'description': 'Updated Description',
            'status': 'IN_PROGRESS',
            'reported_by': self.driver_user.id
        }
        
        response = self.client.post(
            reverse('emergency_update', kwargs={'pk': self.incident.pk}), 
            data,
            follow=True
        )
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('updated successfully' in str(message) for message in messages))

    def test_emergency_incident_delete_view_permission_admin(self):
        """Test that admin can delete incidents."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.post(
            reverse('emergency_delete', kwargs={'pk': self.incident.pk})
        )
        
        self.assertEqual(response.status_code, 302)
        
        # Check that incident was deleted
        self.assertFalse(
            EmergencyIncident.objects.filter(pk=self.incident.pk).exists()
        )

    def test_emergency_incident_delete_view_permission_denied(self):
        """Test that regular users cannot delete incidents."""
        self.client.force_authenticate(user=self.driver_user)
        
        response = self.client.get(
            reverse('emergency_delete', kwargs={'pk': self.incident.pk})
        )
        
        # Should be forbidden
        self.assertEqual(response.status_code, 403)

    def test_emergency_incident_delete_view_success_message(self):
        """Test that delete view shows success message."""
        self.client.force_authenticate(user=self.admin_user)
        
        response = self.client.post(
            reverse('emergency_delete', kwargs={'pk': self.incident.pk}),
            follow=True
        )
        
        messages = list(get_messages(response.wsgi_request))
        self.assertTrue(any('deleted successfully' in str(message) for message in messages))

    def test_emergency_response_create_view_sets_responder(self):
        """Test that response create view sets responder to current user."""
        self.client.force_authenticate(user=self.emergency_user)
        
        data = {
            'incident': self.incident.id,
            'response_type': 'FIRE_DEPARTMENT',
            'description': 'Fire department response'
        }
        
        response = self.client.post(reverse('emergency_response_create'), data)
        
        # Should redirect on success
        self.assertEqual(response.status_code, 302)
        
        # Check that response was created with correct responder
        emergency_response = EmergencyResponse.objects.get(
            description='Fire department response'
        )
        self.assertEqual(emergency_response.responder, self.emergency_user)

    def test_emergency_views_require_login(self):
        """Test that all emergency views require login."""
        urls = [
            reverse('emergency_list'),
            reverse('emergency_detail', kwargs={'pk': self.incident.pk}),
            reverse('emergency_create'),
            reverse('emergency_update', kwargs={'pk': self.incident.pk}),
            reverse('emergency_delete', kwargs={'pk': self.incident.pk}),
        ]
        
        for url in urls:
            response = self.client.get(url)
            # Should redirect to login or return 401/403
            self.assertIn(response.status_code, [302, 401, 403])

    def test_emergency_incident_context_object_names(self):
        """Test that views use correct context object names."""
        self.client.force_authenticate(user=self.admin_user)
        
        # List view
        response = self.client.get(reverse('emergency_list'))
        self.assertIn('incidents', response.context)
        
        # Detail view
        response = self.client.get(reverse('emergency_detail', kwargs={'pk': self.incident.pk}))
        self.assertIn('incident', response.context)

    def test_emergency_incident_templates(self):
        """Test that views use correct templates."""
        self.client.force_authenticate(user=self.admin_user)
        
        # List view
        response = self.client.get(reverse('emergency_list'))
        self.assertTemplateUsed(response, 'emergency/emergency_list.html')
        
        # Detail view
        response = self.client.get(reverse('emergency_detail', kwargs={'pk': self.incident.pk}))
        self.assertTemplateUsed(response, 'emergency/emergency_detail.html')
        
        # Create view
        response = self.client.get(reverse('emergency_create'))
        self.assertTemplateUsed(response, 'emergency/emergency_form.html')
        
        # Update view
        response = self.client.get(reverse('emergency_update', kwargs={'pk': self.incident.pk}))
        self.assertTemplateUsed(response, 'emergency/emergency_form.html')
        
        # Delete view
        response = self.client.get(reverse('emergency_delete', kwargs={'pk': self.incident.pk}))
        self.assertTemplateUsed(response, 'emergency/emergency_confirm_delete.html')