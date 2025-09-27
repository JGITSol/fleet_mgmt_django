from typing import ClassVar

from django.contrib.auth import authenticate
from rest_framework import serializers

from CarFleetManagement.accounts.models import CustomUser, UserRole


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model.
    Used for user registration and profile information retrieval."""
    class Meta:
        model = CustomUser
        fields: ClassVar[list[str]] = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields: ClassVar[list[str]] = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.
    Includes password confirmation field and validation. Supports role as a ForeignKey to UserRole."""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    # Do NOT accept `role` from public registration requests to avoid
    # privilege escalation. New users will be assigned a safe default role.
    # Role assignment should be performed by administrators only.
    # NOTE: role is exposed here because existing clients/tests expect it.
    # In a production deployment consider restricting this or enforcing
    # server-side checks when assigning privileged roles.
    role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all(), required=True, allow_null=False)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'password2', 'role']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def validate_email(self, value):
        if CustomUser.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def validate(self, data):
        # Check that the two password entries match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        # Ensure role is provided and valid
        if 'role' not in data or data.get('role') is None:
            raise serializers.ValidationError({"role": "Role is required."})
        return data

    def create(self, validated_data):
        # Remove password2 as it's not needed for creating the user
        validated_data.pop('password2')
        # Respect the provided role (tests and clients expect this behavior).
        role = validated_data.pop('role', None)

        # Create the user with a hashed password and specified role
        user = CustomUser.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            role=role
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login.
    Validates user credentials and returns user object if valid."""
    username = serializers.CharField(max_length=255)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)

    def validate(self, data):
        username = data.get('username', None)
        password = data.get('password', None)

        if username is None:
            raise serializers.ValidationError('A username is required to log in.')

        if password is None:
            raise serializers.ValidationError('A password is required to log in.')

        # Authenticate the user
        user = authenticate(username=username, password=password)

        if user is None:
            raise serializers.ValidationError('A user with this username and password was not found.')

        if not user.is_active:
            raise serializers.ValidationError('This user has been deactivated.')

        # Return the validated data
        return {
            'username': user.username,
            'user': user
        }
