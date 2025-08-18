import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from CarFleetManagement.accounts.models import UserRole, CustomUser
from tests.auth_utils import get_authenticated_client

@pytest.mark.django_db
def test_register_valid():
    client = APIClient()
    url = reverse('CarFleetManagement.api:api_register')
    # Ensure role exists
    driver_role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER, defaults={'description': 'Driver role'})
    data = {
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'StrongPassword123!',
        'password2': 'StrongPassword123!',
        'role': driver_role.id,
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_201_CREATED
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['user']['username'] == 'newuser'

@pytest.mark.django_db
def test_register_missing_fields():
    client = APIClient()
    url = reverse('CarFleetManagement.api:api_register')
    data = {
        'username': '',
        'email': '',
        'password': '',
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'username' in response.data or 'email' in response.data or 'password' in response.data

@pytest.mark.django_db
def test_register_duplicate_email():
    client = APIClient()
    url = reverse('CarFleetManagement.api:api_register')
    admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, defaults={'description': 'Administrator role'})
    user = CustomUser.objects.create_user(
        username='existing',
        email='existing@example.com',
        password='password',
        role=admin_role
    )
    driver_role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER, defaults={'description': 'Driver role'})
    data = {
        'username': 'another',
        'email': 'existing@example.com',
        'password': 'AnotherPassword123!',
        'password2': 'AnotherPassword123!',
        'role': driver_role.id,
    }
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'email' in response.data

@pytest.mark.django_db
def test_login_valid():
    client = APIClient()
    admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, defaults={'description': 'Administrator role'})
    user = CustomUser.objects.create_user(
        username='loginuser',
        email='loginuser@example.com',
        password='MySecret123!',
        role=admin_role
    )
    url = reverse('CarFleetManagement.api:api_login')
    data = {'username': 'loginuser', 'password': 'MySecret123!'}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data
    assert 'refresh' in response.data
    assert response.data['user']['username'] == 'loginuser'

@pytest.mark.django_db
def test_login_invalid_password():
    client = APIClient()
    admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN, defaults={'description': 'Administrator role'})
    user = CustomUser.objects.create_user(
        username='loginuser2',
        email='loginuser2@example.com',
        password='MySecret123!',
        role=admin_role
    )
    url = reverse('CarFleetManagement.api:api_login')
    data = {'username': 'loginuser2', 'password': 'WrongPassword!'}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data or 'password' in response.data

@pytest.mark.django_db
def test_login_nonexistent_user():
    client = APIClient()
    url = reverse('CarFleetManagement.api:api_login')
    data = {'username': 'doesnotexist', 'password': 'irrelevant'}
    response = client.post(url, data)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert 'non_field_errors' in response.data or 'username' in response.data

@pytest.mark.django_db
def test_logout():
    client, user = get_authenticated_client()
    url = reverse('CarFleetManagement.api:api_logout')
    response = client.post(url)
    assert response.status_code == status.HTTP_200_OK
    assert 'message' in response.data

@pytest.mark.django_db
def test_token_validation():
    client, user = get_authenticated_client()
    url = reverse('CarFleetManagement.api:api_validate_token')
    response = client.get(url)
    assert response.status_code == status.HTTP_200_OK
    assert response.data['is_valid'] is True
    assert response.data['user']['username'] == user.username

@pytest.mark.django_db
def test_profile_requires_auth():
    client = APIClient()
    url = reverse('CarFleetManagement.api:api_profile')
    response = client.get(url)
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
