from django.contrib.auth.forms import UserCreationForm

from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    # Inherit Meta from UserCreationForm to avoid including password fields
    # or other non-model fields in Meta.fields. Do NOT expose `role` here
    # so public registration cannot set privileged roles.
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            'username', 'email', 'role', 'phone_number', 'emergency_contact'
        )
