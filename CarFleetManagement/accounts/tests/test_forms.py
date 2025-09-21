"""
Tests for accounts forms.
"""
from django.test import TestCase

from CarFleetManagement.accounts.forms import CustomUserCreationForm
from CarFleetManagement.accounts.models import UserRole


class CustomUserCreationFormTestCase(TestCase):
    """Test cases for CustomUserCreationForm."""

    def setUp(self):
        """Set up test data."""
        self.admin_role = UserRole.objects.create(
            name='ADMIN',
            description='Administrator role'
        )
        self.driver_role = UserRole.objects.create(
            name='DRIVER',
            description='Driver role'
        )

    def test_form_valid_data(self):
        """Test form with valid data."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': self.driver_role.id,
            'phone_number': '+1234567890',
            'emergency_contact': 'John Doe - +0987654321',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        """Test form with mismatched passwords."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': self.driver_role.id,
            'phone_number': '+1234567890',
            'emergency_contact': 'John Doe - +0987654321',
            'password1': 'testpass123',
            'password2': 'differentpass',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password2', form.errors)

    def test_form_missing_required_fields(self):
        """Test form with missing required fields."""
        form_data = {
            'username': 'testuser',
            # Missing email, role, passwords
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('password1', form.errors)
        self.assertIn('password2', form.errors)

    def test_form_invalid_email(self):
        """Test form with invalid email."""
        form_data = {
            'username': 'testuser',
            'email': 'invalid-email',
            'role': self.driver_role.id,
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('email', form.errors)

    def test_form_save(self):
        """Test form save creates user correctly."""
        form_data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'role': self.admin_role.id,
            'phone_number': '+1234567890',
            'emergency_contact': 'John Doe - +0987654321',
            'password1': 'testpass123',
            'password2': 'testpass123',
        }
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        
        user = form.save()
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.role, self.admin_role)
        self.assertEqual(user.phone_number, '+1234567890')
        self.assertEqual(user.emergency_contact, 'John Doe - +0987654321')
        self.assertTrue(user.check_password('testpass123'))

    def test_form_fields_included(self):
        """Test that all expected fields are included in the form."""
        form = CustomUserCreationForm()
        expected_fields = [
            'username', 'email', 'role', 'phone_number', 
            'emergency_contact', 'password1', 'password2'
        ]
        for field in expected_fields:
            self.assertIn(field, form.fields)