from typing import ClassVar

from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from CarFleetManagement.accounts.models import UserRole
from .serializers import LoginSerializer, UserRegistrationSerializer, UserSerializer


class RegisterView(APIView):
    """API view for user registration.

    Allows new users to register with the application.
    """

    permission_classes: ClassVar[list] = [AllowAny]

    def post(self, request):
        """
        Register a new user and return JWT tokens.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request containing registration data.

        Returns
        -------
        rest_framework.response.Response
            JSON with user data and JWT tokens or validation errors.
        """
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate JWT tokens for the new user
            refresh = RefreshToken.for_user(user)
            return Response(
                {"user": UserSerializer(user).data, "refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """API view for user login.

    Authenticates user credentials and returns a token.
    """

    permission_classes: ClassVar[list] = [AllowAny]

    def post(self, request):
        """
        Register a new user and return JWT tokens.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request containing registration data.

        Returns
        -------
        rest_framework.response.Response
            JSON with user data and JWT tokens or validation errors.
        """
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data["user"]
            # Generate JWT tokens for the user
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    """API view for retrieving user profile information.

    Requires authentication token.
    """

    permission_classes: ClassVar[list] = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the authenticated user's profile.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request (must be authenticated).

        Returns
        -------
        rest_framework.response.Response
            JSON with user profile data.
        """
        serializer = UserSerializer(request.user)
        return Response({"user": serializer.data})


class LogoutView(APIView):
    """API view for user logout.

    Deletes the user's authentication token.
    """

    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request):
        """
        Register a new user and return JWT tokens.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request containing registration data.

        Returns
        -------
        rest_framework.response.Response
            JSON with user data and JWT tokens or validation errors.
        """
        # For JWT, logout is handled client-side by deleting the token. If using JWT blacklist, blacklist the refresh token here.

        return Response(
            {"message": "Successfully logged out (JWT token deleted on client)."}, status=status.HTTP_200_OK
        )


class ValidateTokenView(APIView):
    """API view for validating authentication tokens.

    Used by the Lynx mobile app to check if a stored token is still valid.
    """

    permission_classes: ClassVar[list] = [IsAuthenticated]

    def get(self, request):
        """
        Retrieve the authenticated user's profile.

        Parameters
        ----------
        request : rest_framework.request.Request
            The HTTP request (must be authenticated).

        Returns
        -------
        rest_framework.response.Response
            JSON with user profile data.
        """
        return Response({"is_valid": True, "user": UserSerializer(request.user).data})


class SwitchRoleView(APIView):
    """
    Allow test users to switch their role dynamically for testing UI scopes.
    """

    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request):
        role_name = request.data.get('role')
        if not role_name:
            return Response({"error": "Role name required"}, status=status.HTTP_400_BAD_REQUEST)

        # Security check: only superusers or people already in testuser role can switch
        is_test_user = getattr(request.user.role, 'name', None) == UserRole.TESTUSER
        if not (request.user.is_superuser or is_test_user):
            return Response(
                {"error": "Only test users or admins can switch roles"}, status=status.HTTP_403_FORBIDDEN
            )

        try:
            new_role = UserRole.objects.get(name=role_name)
            request.user.role = new_role
            request.user.save()
            return Response({"message": f"Switched to role: {role_name}", "user": UserSerializer(request.user).data})
        except UserRole.DoesNotExist:
            return Response({"error": f"Role '{role_name}' not found"}, status=status.HTTP_404_NOT_FOUND)
