"""
Tests for API serializers.
"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.utils import timezone

from CarFleetManagement.api.serializers import (
    UserSerializer, UserRegistrationSerializer, LoginSerializer
)
from CarFleetManagement.accounts.models import UserRole

User = get_user_model()


class UserSerializerTestCase(TestCase):
    """Test cases for UserSerializer."""

    def setUp(self):
        """Set up test data."""
        self.driver_role, _ = UserRole.objects.get_or_create(
            name='DRIVER',
            defaults={'description': 'Driver role'}
        )

        unique_username = f"testuser_{timezone.now().timestamp():.0f}"
        self.test_user = User.objects.create_user(
            username=unique_username,
            email=f"{unique_username}@example.com",
            password='testpass123',
            first_name='Test',
            last_name='User',
            role=self.driver_role
        )

    def test_user_serializer_fields(self):
        """Test that UserSerializer includes correct fields."""
        serializer = UserSerializer(instance=self.test_user)
        data = serializer.data
        
        expected_fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        for field in expected_fields:
            self.assertIn(field, data)
        
        self.assertEqual(data['username'], self.test_user.username)
        self.assertEqual(data['email'], self.test_user.email)
        self.assertEqual(data['first_name'], 'Test')
        self.assertEqual(data['last_name'], 'User')
        self.assertEqual(data['role'], self.driver_role.id)

    def test_user_serializer_read_only_fields(self):
        """Test that id field is read-only."""
        serializer = UserSerializer()
        self.assertIn('id', serializer.Meta.read_only_fields)


class UserRegistrationSerializerTestCase(TestCase):
    """Test cases for UserRegistrationSerializer."""

    def setUp(self):
        """Set up test data."""
        self.admin_role, _ = UserRole.objects.get_or_create(
            name='ADMIN',
            defaults={'description': 'Administrator role'}
        )
        self.driver_role, _ = UserRole.objects.get_or_create(
            name='DRIVER',
            defaults={'description': 'Driver role'}
        )

    def test_valid_registration_data(self):
        """Test serializer with valid registration data."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'role': self.driver_role.id
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_password_mismatch(self):
        """Test serializer with mismatched passwords."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'differentpass',
            'role': self.driver_role.id
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_duplicate_email_validation(self):
        """Test validation for duplicate email."""
        # Create existing user
        User.objects.create_user(
            username='existing',
            email='existing@example.com',
            password='pass123',
            role=self.driver_role
        )
        
        data = {
            'username': 'newuser',
            'email': 'existing@example.com',  # Duplicate email
            'password': 'newpass123',
            'password2': 'newpass123',
            'role': self.driver_role.id
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('email', serializer.errors)
        self.assertIn('already exists', str(serializer.errors['email'][0]))

    def test_missing_required_fields(self):
        """Test serializer with missing required fields."""
        data = {
            'username': 'newuser',
            # Missing email, password, password2, role
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertIn('password2', serializer.errors)
        self.assertIn('role', serializer.errors)

    def test_invalid_role(self):
        """Test serializer with invalid role."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'role': 99999  # Non-existent role ID
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('role', serializer.errors)

    def test_create_user(self):
        """Test creating user through serializer."""
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'role': self.admin_role.id
        }
        
        serializer = UserRegistrationSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        user = serializer.save()
        
        self.assertEqual(user.username, 'newuser')
        self.assertEqual(user.email, 'newuser@example.com')
        self.assertEqual(user.role, self.admin_role)
        self.assertTrue(user.check_password('newpass123'))
        self.assertTrue(user.is_active)

    def test_password_write_only(self):
        """Test that password fields are write-only."""
        serializer = UserRegistrationSerializer()
        self.assertTrue(serializer.fields['password'].write_only)
        self.assertTrue(serializer.fields['password2'].write_only)

    def test_role_queryset(self):
        """Test that role field uses correct queryset."""
        serializer = UserRegistrationSerializer()
        role_field = serializer.fields['role']
        
        # Check that queryset includes our test roles
        role_ids = [role.id for role in role_field.queryset]
        self.assertIn(self.admin_role.id, role_ids)
        self.assertIn(self.driver_role.id, role_ids)


class LoginSerializerTestCase(TestCase):
    """Test cases for LoginSerializer."""

    def setUp(self):
        """Set up test data."""
        self.driver_role, _ = UserRole.objects.get_or_create(
            name='DRIVER',
            defaults={'description': 'Driver role'}
        )

        unique_username = f"testuser_{timezone.now().timestamp():.0f}"
        self.test_user = User.objects.create_user(
            username=unique_username,
            email=f"{unique_username}@example.com",
            password='testpass123',
            role=self.driver_role
        )

        self.inactive_user = User.objects.create_user(
            username=f'inactive_{timezone.now().timestamp():.0f}',
            email=f"inactive_{timezone.now().timestamp():.0f}@example.com",
            password='testpass123',
            role=self.driver_role,
            is_active=False
        )

    def test_valid_login_data(self):
        """Test serializer with valid login credentials."""
        data = {
            'username': self.test_user.username,
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        
        validated_data = serializer.validated_data
        self.assertEqual(validated_data['username'], self.test_user.username)
        self.assertEqual(validated_data['user'], self.test_user)

    def test_invalid_username(self):
        """Test serializer with invalid username."""
        data = {
            'username': 'nonexistent',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('not found', str(serializer.errors['non_field_errors'][0]))

    def test_invalid_password(self):
        """Test serializer with invalid password."""
        data = {
            'username': self.test_user.username,
            'password': 'wrongpassword'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)
        self.assertIn('not found', str(serializer.errors['non_field_errors'][0]))

    def test_missing_username(self):
        """Test serializer with missing username."""
        data = {
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_missing_password(self):
        """Test serializer with missing password."""
        data = {
            'username': self.test_user.username
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_inactive_user(self):
        """Test serializer with inactive user."""
        data = {
            'username': self.inactive_user.username,
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('non_field_errors', serializer.errors)

    def test_empty_username(self):
        """Test serializer with empty username."""
        data = {
            'username': '',
            'password': 'testpass123'
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)

    def test_empty_password(self):
        """Test serializer with empty password."""
        data = {
            'username': self.test_user.username,
            'password': ''
        }
        
        serializer = LoginSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)

    def test_token_field_read_only(self):
        """Test that token field is read-only."""
        serializer = LoginSerializer()
        self.assertTrue(serializer.fields['token'].read_only)

    def test_password_field_write_only(self):
        """Test that password field is write-only."""
        serializer = LoginSerializer()
        self.assertTrue(serializer.fields['password'].write_only)