"""
Tests for API authentication views.
"""
from django.contrib.auth import get_user_model
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from CarFleetManagement.accounts.models import UserRole

User = get_user_model()


class AuthViewsTestCase(APITestCase):
    """Test cases for authentication API views."""

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
        
        self.test_user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            role=self.driver_role
        )

    def test_register_view_success(self):
        """Test successful user registration."""
        url = reverse('CarFleetManagement.api:api_register')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',  # Changed from password_confirm to password2
            'role': self.driver_role.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'newuser')
        self.assertEqual(response.data['user']['email'], 'newuser@example.com')

    def test_register_view_invalid_data(self):
        """Test registration with invalid data."""
        url = reverse('CarFleetManagement.api:api_register')
        data = {
            'username': '',  # Empty username
            'email': 'invalid-email',  # Invalid email
            'password': 'short',  # Too short password
            'password_confirm': 'different',  # Different confirmation
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('username', response.data)

    def test_register_view_duplicate_username(self):
        """Test registration with duplicate username."""
        url = reverse('CarFleetManagement.api:api_register')
        data = {
            'username': 'testuser',  # Already exists
            'email': 'different@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',  # Changed from password_confirm to password2
            'role': self.driver_role.id
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        """Test successful user login."""
        url = reverse('CarFleetManagement.api:api_login')
        data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('user', response.data)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_login_view_invalid_credentials(self):
        """Test login with invalid credentials."""
        url = reverse('CarFleetManagement.api:api_login')
        data = {
            'username': 'testuser',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_missing_data(self):
        """Test login with missing data."""
        url = reverse('CarFleetManagement.api:api_login')
        data = {
            'username': 'testuser'
            # Missing password
        }
        response = self.client.post(url, data, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.data)

    def test_user_profile_view_authenticated(self):
        """Test user profile view with authentication."""
        # Get JWT token
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        
        url = reverse('CarFleetManagement.api:api_profile')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['username'], 'testuser')
        self.assertEqual(response.data['email'], 'test@example.com')

    def test_user_profile_view_unauthenticated(self):
        """Test user profile view without authentication."""
        url = reverse('CarFleetManagement.api:api_profile')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_view_authenticated(self):
        """Test logout view with authentication."""
        # Get JWT token
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        
        url = reverse('CarFleetManagement.api:api_logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response.data)

    def test_logout_view_unauthenticated(self):
        """Test logout view without authentication."""
        url = reverse('CarFleetManagement.api:api_logout')
        response = self.client.post(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_token_view_valid_token(self):
        """Test token validation with valid token."""
        # Get JWT token
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        
        url = reverse('CarFleetManagement.api:api_validate_token')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['is_valid'])
        self.assertEqual(response.data['user']['username'], 'testuser')

    def test_validate_token_view_invalid_token(self):
        """Test token validation with invalid token."""
        url = reverse('CarFleetManagement.api:api_validate_token')
        self.client.credentials(HTTP_AUTHORIZATION='Bearer invalid_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_validate_token_view_no_token(self):
        """Test token validation without token."""
        url = reverse('CarFleetManagement.api:api_validate_token')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)