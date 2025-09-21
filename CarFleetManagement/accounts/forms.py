from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            'username', 'email', 'role', 'phone_number', 'emergency_contact',
            'password1', 'password2'
        )
