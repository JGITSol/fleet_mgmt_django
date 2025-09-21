"""
Tests for API middleware.
"""
from unittest.mock import Mock, patch

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpRequest, HttpResponse
from django.test import TestCase
from rest_framework_simplejwt.tokens import RefreshToken

from CarFleetManagement.api.middleware import JWTAuthMiddleware
from CarFleetManagement.accounts.models import UserRole

User = get_user_model()


class JWTAuthMiddlewareTestCase(TestCase):
    """Test cases for JWT authentication middleware."""

    def setUp(self):
        """Set up test data."""
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
        
        # Create a mock get_response function
        self.get_response = Mock(return_value=HttpResponse())
        self.middleware = JWTAuthMiddleware(self.get_response)

    def test_middleware_with_valid_jwt_token(self):
        """Test middleware with valid JWT token."""
        # Generate JWT token
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        
        # Create request with JWT token
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user was authenticated
        self.assertEqual(request.user, self.test_user)
        self.assertTrue(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_with_invalid_jwt_token(self):
        """Test middleware with invalid JWT token."""
        # Create request with invalid JWT token
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer invalid_token'
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains anonymous
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_without_authorization_header(self):
        """Test middleware without Authorization header."""
        # Create request without Authorization header
        request = HttpRequest()
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains anonymous
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_with_non_bearer_authorization(self):
        """Test middleware with non-Bearer authorization."""
        # Create request with non-Bearer authorization
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Basic dGVzdDp0ZXN0'
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains anonymous
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_with_already_authenticated_user(self):
        """Test middleware when user is already authenticated."""
        # Create request with already authenticated user
        request = HttpRequest()
        request.user = self.test_user
        
        # Generate JWT token (should be ignored)
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains the same
        self.assertEqual(request.user, self.test_user)
        self.assertTrue(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_with_malformed_bearer_token(self):
        """Test middleware with malformed Bearer token."""
        # Create request with malformed Bearer token
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer'  # Missing token
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains anonymous
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    @patch('CarFleetManagement.api.middleware.JWTAuthentication')
    def test_middleware_with_jwt_authentication_exception(self, mock_jwt_auth):
        """Test middleware when JWT authentication raises an exception."""
        # Mock JWT authentication to raise an exception
        mock_auth_instance = Mock()
        mock_auth_instance.authenticate.side_effect = Exception('JWT error')
        mock_jwt_auth.return_value = mock_auth_instance
        
        # Create request with JWT token
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = 'Bearer some_token'
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that user remains anonymous (exception was caught)
        self.assertIsInstance(request.user, AnonymousUser)
        self.assertFalse(request.user.is_authenticated)
        self.get_response.assert_called_once_with(request)

    def test_middleware_sets_cached_user(self):
        """Test that middleware sets both user and _cached_user."""
        # Generate JWT token
        refresh = RefreshToken.for_user(self.test_user)
        access_token = str(refresh.access_token)
        
        # Create request with JWT token
        request = HttpRequest()
        request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'
        request.user = AnonymousUser()
        
        # Process request through middleware
        response = self.middleware(request)
        
        # Check that both user and _cached_user are set
        self.assertEqual(request.user, self.test_user)
        self.assertEqual(request._cached_user, self.test_user)