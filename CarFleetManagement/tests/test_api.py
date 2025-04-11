import pytest
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

# Import tests from the app-specific test directory
from api.tests.test_report_generator import ScreenshotAnalysisReportTestCase
from api.tests.test_openrouter_client import *
from api.tests.test_views import *
from api.tests.test_management_commands import *

User = get_user_model()


# Add additional tests that might require fixtures from conftest.py
@pytest.mark.django_db
def test_api_authentication(user):
    """Test API authentication."""
    client = APIClient()
    
    # Attempt unauthenticated access
    response = client.get(reverse('api:vehicle-list'))
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
    
    # Authenticate and try again
    client.force_authenticate(user=user)
    response = client.get(reverse('api:vehicle-list'))
    assert response.status_code == status.HTTP_200_OK


@pytest.mark.django_db
def test_vehicle_api_endpoints(vehicle, user):
    """Test vehicle API endpoints."""
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Test listing vehicles
    response = client.get(reverse('api:vehicle-list'))
    assert response.status_code == status.HTTP_200_OK
    assert len(response.data) >= 1
    
    # Test retrieving a specific vehicle
    response = client.get(reverse('api:vehicle-detail', kwargs={'pk': vehicle.id}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['brand'] == 'Toyota'
    assert response.data['model'] == 'Camry'


@pytest.mark.django_db
def test_maintenance_api_endpoints(maintenance_record, user):
    """Test maintenance API endpoints."""
    client = APIClient()
    client.force_authenticate(user=user)
    
    # Test listing maintenance records
    response = client.get(reverse('api:maintenance-list'))
    assert response.status_code == status.HTTP_200_OK
    
    # Test retrieving a specific maintenance record
    response = client.get(reverse('api:maintenance-detail', kwargs={'pk': maintenance_record.id}))
    assert response.status_code == status.HTTP_200_OK
    assert response.data['service_type'] == 'Oil Change'
    assert float(response.data['cost']) == 50.00