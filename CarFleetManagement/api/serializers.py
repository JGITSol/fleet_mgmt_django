from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class UserSerializer(serializers.ModelSerializer):
    """Serializer for the User model.
    
    Used for user registration and profile information retrieval.
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        read_only_fields = ['id']


class UserRegistrationSerializer(serializers.ModelSerializer):
    """Serializer for user registration.
    
    Includes password confirmation field and validation.
    """
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2']
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data):
        # Check that the two password entries match
        if data['password'] != data['password2']:
            raise serializers.ValidationError({"password": "Passwords don't match."})
        return data
    
    def create(self, validated_data):
        # Remove password2 as it's not needed for creating the user
        validated_data.pop('password2')
        
        # Create the user with a hashed password
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class LoginSerializer(serializers.Serializer):
    """Serializer for user login.
    
    Validates user credentials and returns user object if valid.
    """
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