import pytest
from django.contrib.auth import get_user_model

# No need to import tests from the app-specific test directory
# We'll focus on basic model testing instead

User = get_user_model()


# Simple test to verify the User model works
@pytest.mark.django_db
def test_user_creation(user):
    """Test that the user fixture works correctly."""
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'

    # Create another user manually
    new_user = User.objects.create_user(
        username='testuser2',
        email='test2@example.com',
        password='testpassword2'
    )
    assert User.objects.count() >= 2
    assert new_user.username == 'testuser2'
