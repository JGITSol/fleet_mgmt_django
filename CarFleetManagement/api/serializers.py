from rest_framework import serializers
from accounts.models import CustomUser, UserRole
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the CustomUser model.
    Used for user registration and profile information retrieval."""
    class Meta:
        model = CustomUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.
    Includes password confirmation field and validation. Supports role as a ForeignKey to UserRole."""
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    role = serializers.PrimaryKeyRelatedField(queryset=UserRole.objects.all())

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
        return data

    def create(self, validated_data):
        # Remove password2 as it's not needed for creating the user
        validated_data.pop('password2')
        role = validated_data.pop('role')
        # Create the user with a hashed password and role
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