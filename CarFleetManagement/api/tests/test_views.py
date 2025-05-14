import os
import json
from rest_framework_simplejwt.tokens import RefreshToken
from unittest import mock
from django.urls import reverse
from rest_framework.test import APITestCase
from django.conf import settings
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from accounts.models import CustomUser, UserRole
from .jwt_test_mixin import JWTAuthTestMixin


class AnalyzeScreenshotViewTestCase(JWTAuthTestMixin, APITestCase):
    """Test cases for the AnalyzeScreenshotView."""
    
    def setUp(self):
        """Set up test environment."""
        # Authenticate as admin user for all API requests
        self.admin_user = self.authenticate_client(role_name='ADMIN')
        self.url = reverse('CarFleetManagement.api:analyze_screenshot')
        # Create a valid PNG image in memory for upload
        from io import BytesIO
        from PIL import Image
        image_io = BytesIO()
        img = Image.new('RGB', (10, 10), color=(255, 0, 0))
        img.save(image_io, format='PNG')
        image_io.seek(0)
        self.image_content = image_io.getvalue()
        self.test_image = SimpleUploadedFile(
            name='test_screenshot.png',
            content=self.image_content,
            content_type='image/png'
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Ensure temp directory is cleaned up robustly
        import shutil
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_screenshots')
        if os.path.exists(temp_dir):
            try:
                shutil.rmtree(temp_dir)
            except Exception:
                pass
    
    def test_post_without_screenshot(self):
        """Test POST request without screenshot file."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_screenshot(self, mock_get_client):
        """Test POST request with screenshot file."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(
            self.url,
            {'screenshot': self.test_image},
            format='multipart'
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('choices', response.data)
        
        # Verify the client was called correctly
        mock_client.analyze_screenshot.assert_called_once()
        args, kwargs = mock_client.analyze_screenshot.call_args
        self.assertEqual(kwargs['prompt'], None)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_screenshot_and_prompt(self, mock_get_client):
        """Test POST request with screenshot file and custom prompt."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(
            self.url,
            {
                'screenshot': self.test_image,
                'prompt': 'Custom prompt'
            },
            format='multipart'
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify the client was called with the custom prompt
        mock_client.analyze_screenshot.assert_called_once()
        args, kwargs = mock_client.analyze_screenshot.call_args
        self.assertEqual(kwargs['prompt'], 'Custom prompt')
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_client_error(self, mock_get_client):
        """Test POST request with client error."""
        # Mock the OpenRouter client to raise an exception
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.side_effect = Exception('Test error')
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(
            self.url,
            {'screenshot': self.test_image},
            format='multipart'
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Test error')


class BatchAnalyzeScreenshotsViewTestCase(JWTAuthTestMixin, APITestCase):
    """Test cases for the BatchAnalyzeScreenshotsView."""
    
    def setUp(self):
        """Set up test environment."""
        # Authenticate as admin user for all API requests
        self.admin_user = self.authenticate_client(role_name='ADMIN')
        self.url = reverse('CarFleetManagement.api:batch_analyze_screenshots')
        # Create a test screenshots directory
        self.screenshots_dir = os.path.join(settings.BASE_DIR, 'debug_screenshots')
        os.makedirs(self.screenshots_dir, exist_ok=True)
        # Create test screenshot files
        self.test_screenshots = [
            'home_en_dark_20250331-201208.png',
            'home_en_light_20250331-201203.png',
            'about_fr_dark_20250331-201239.png',
            'features_es_light_20250331-201220.png'
        ]
        for screenshot in self.test_screenshots:
            with open(os.path.join(self.screenshots_dir, screenshot), 'w') as f:
                f.write('test image content')
    
    def tearDown(self):
        """Clean up test environment."""
        # Remove test screenshot files
        for screenshot in self.test_screenshots:
            file_path = os.path.join(self.screenshots_dir, screenshot)
            if os.path.exists(file_path):
                os.remove(file_path)
        
        # Remove test directory if it's empty
        if os.path.exists(self.screenshots_dir) and not os.listdir(self.screenshots_dir):
            os.rmdir(self.screenshots_dir)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_without_filters(self, mock_get_client):
        """Test POST request without filters."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(self.url, {})
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 4)  # All 4 screenshots
        
        # Verify the client was called for each screenshot
        self.assertEqual(mock_client.analyze_screenshot.call_count, 4)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_language_filter(self, mock_get_client):
        """Test POST request with language filter."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(self.url, {'language': 'en'})
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only the 2 English screenshots
        self.assertIn('home_en_dark_20250331-201208.png', response.data)
        self.assertIn('home_en_light_20250331-201203.png', response.data)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_theme_filter(self, mock_get_client):
        """Test POST request with theme filter."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(self.url, {'theme': 'dark'})
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only the 2 dark theme screenshots
        self.assertIn('home_en_dark_20250331-201208.png', response.data)
        self.assertIn('about_fr_dark_20250331-201239.png', response.data)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_page_filter(self, mock_get_client):
        """Test POST request with page filter."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(self.url, {'page': 'home'})
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Only the 2 home page screenshots
        self.assertIn('home_en_dark_20250331-201208.png', response.data)
        self.assertIn('home_en_light_20250331-201203.png', response.data)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_multiple_filters(self, mock_get_client):
        """Test POST request with multiple filters."""
        # Mock the OpenRouter client
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(
            self.url,
            {
                'language': 'en',
                'theme': 'dark'
            }
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only the English dark theme screenshot
        self.assertIn('home_en_dark_20250331-201208.png', response.data)
    
    def test_post_with_no_matching_screenshots(self):
        """Test POST request with filters that match no screenshots."""
        # Make the request
        response = self.client.post(
            self.url,
            {
                'language': 'de',  # No German screenshots
                'theme': 'dark'
            }
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('warning', response.data)
    
    @mock.patch('CarFleetManagement.api.views.get_client')
    def test_post_with_client_error(self, mock_get_client):
        """Test POST request with client error."""
        # Mock the OpenRouter client to raise an exception
        mock_client = mock.Mock()
        mock_client.analyze_screenshot.side_effect = Exception('Test error')
        mock_get_client.return_value = mock_client
        
        # Make the request
        response = self.client.post(self.url, {})
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)


class GenerateReportViewTestCase(JWTAuthTestMixin, APITestCase):
    """Test cases for the GenerateReportView."""

    def setUp(self):
        """Set up test environment."""
        # Authenticate as admin user for all API requests
        self.admin_user = self.authenticate_client(role_name='ADMIN')
        self.url = reverse('CarFleetManagement.api:generate_report')
        # Create test analysis data
        self.analysis_data = {
            'home_en_dark_20250331-201208.png': {
                'choices': [
                    {
                        'message': {
                            'content': 'Analysis for home page in English with dark theme'
                        }
                    }
                ]
            },
            'home_en_light_20250331-201203.png': {
                'choices': [
                    {
                        'message': {
                            'content': 'Analysis for home page in English with light theme'
                        }
                    }
                ]
            }
        }

    def tearDown(self):
        """Clean up test environment."""
        # Ensure temp directory is cleaned up
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_analysis')
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
    
    def test_post_without_analysis_data(self):
        """Test POST request without analysis data."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    @mock.patch('CarFleetManagement.api.views.generate_report')
    def test_post_with_analysis_data(self, mock_generate_report):
        """Test POST request with analysis data."""
        # Mock the generate_report function
        report_content = '<html><body>Test Report</body></html>'
        
        # Create a temporary file that will be returned by generate_report
        temp_file = os.path.join(settings.BASE_DIR, 'temp_report.html')
        with open(temp_file, 'w') as f:
            f.write(report_content)
        
        mock_generate_report.return_value = temp_file
        
        # Make the request
        response = self.client.post(
            self.url,
            {'analysis_data': self.analysis_data},
            format='json'
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.content.decode(), report_content)
        self.assertEqual(response['Content-Type'], 'text/html')
        
        # Clean up the temporary file
        if os.path.exists(temp_file):
            os.remove(temp_file)
    
    @mock.patch('CarFleetManagement.api.views.generate_report')
    def test_post_with_generate_report_error(self, mock_generate_report):
        """Test POST request with generate_report error."""
        # Mock the generate_report function to raise an exception
        mock_generate_report.side_effect = Exception('Test error')
        
        # Make the request
        response = self.client.post(
            self.url,
            {'analysis_data': self.analysis_data},
            format='json'
        )
        
        # Verify the response
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)
        self.assertIn('error', response.data)
        self.assertEqual(response.data['error'], 'Test error')


class TestVehicleAPI(JWTAuthTestMixin, APITestCase):
    def setUp(self):
        Vehicle.objects.all().delete()
        self.admin_user = self.authenticate_client(role_name='ADMIN')
        self.url = reverse('CarFleetManagement.api:api-vehicle-list')
        # Create a user role
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN)
        
        # Create a test user with appropriate permissions
        self.user = CustomUser.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword',
            is_staff=True,
            is_superuser=True
        )
        self.user.role = self.admin_role
        self.user.save()
        
        # Authenticate the client using JWTAuthTestMixin (sets JWT token)
        self.authenticate_client(user=self.user, role_name='ADMIN')
        
        self.vehicle_data = {
            'brand': 'Toyota',
            'model': 'Corolla',
            'year': 2020,
            'license_plate': 'XYZ-123',
            'vin': '1HGCM82633A123456'
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)

    def test_vehicle_list(self):
        url = reverse('CarFleetManagement.api:api-vehicle-list')
        response = self.client.get(url)
        vehicles = Vehicle.objects.all()
        serializer = VehicleSerializer(vehicles, many=True)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_vehicle_create(self):
        url = reverse('CarFleetManagement.api:api-vehicle-create')
        # Create data for the new vehicle, ensuring uniqueness for relevant fields
        create_data = self.vehicle_data.copy()
        create_data['license_plate'] = 'NEW-789' # Ensure this is unique
        create_data['vin'] = 'NEWVIN1234567890' # Ensure this is unique

        response = self.client.post(url, create_data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vehicle.objects.count(), 2) # One from setUp, one from this test
        # Verify the newly created vehicle, not the one from setUp
        new_vehicle = Vehicle.objects.get(id=response.data['id'])
        self.assertEqual(new_vehicle.brand, create_data['brand'])
        self.assertEqual(new_vehicle.license_plate, create_data['license_plate'])

    def test_vehicle_detail(self):
        url = reverse('CarFleetManagement.api:api-vehicle-detail', args=[self.vehicle.id])
        response = self.client.get(url)
        serializer = VehicleSerializer(self.vehicle)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_vehicle_update(self):
        url = reverse('CarFleetManagement.api:api-vehicle-update', args=[self.vehicle.id])
        updated_data = self.vehicle_data.copy()
        updated_data['brand'] = 'Honda'
        response = self.client.put(url, updated_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.brand, 'Honda')

    def test_vehicle_delete(self):
        url = reverse('CarFleetManagement.api:api-vehicle-delete', args=[self.vehicle.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vehicle.objects.count(), 0)


class TestVehicleAPIPermissions(JWTAuthTestMixin, APITestCase):
    def setUp(self):
        from accounts.models import UserRole, CustomUser
        from vehicles.models import Vehicle
        Vehicle.objects.all().delete()
        self.admin_user = self.authenticate_client(role_name='ADMIN')
        self.admin_role, _ = UserRole.objects.get_or_create(name=UserRole.ADMIN)
        self.driver_role, _ = UserRole.objects.get_or_create(name=UserRole.DRIVER)
        
        self.jwt_admin_user = CustomUser.objects.create_user(
            username='jwtadmin', email='jwtadmin@example.com', password='adminpass', role=self.admin_role, is_staff=True, is_superuser=True
        )
        self.jwt_driver_user = CustomUser.objects.create_user(
            username='jwtdriver', email='jwtdriver@example.com', password='driverpass', role=self.driver_role
        )

        self.vehicle_data = {
            'brand': 'TestBrand', 'model': 'TestModel', 'year': 2022, 'license_plate': 'PLT-123', 'vin': 'VIN-JWT-123'
        }
        self.vehicle = Vehicle.objects.create(**self.vehicle_data)
        self.list_url = reverse('CarFleetManagement.api:api-vehicle-list')
        self.detail_url = lambda: reverse('CarFleetManagement.api:api-vehicle-detail', args=[self.vehicle.id])

    def get_jwt_token(self, user):
        refresh = RefreshToken.for_user(user)
        return str(refresh.access_token)

    def test_vehicle_list_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 200)

    def test_vehicle_list_non_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_driver_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 403)

    def test_vehicle_list_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, 401)

    def test_vehicle_create_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = self.vehicle_data.copy()
        data['license_plate'] = 'PLT-NEW'
        data['vin'] = 'VIN-JWT-NEW'
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 201)

    def test_vehicle_create_non_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_driver_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = self.vehicle_data.copy()
        data['license_plate'] = 'PLT-NEW2'
        data['vin'] = 'VIN-JWT-NEW2'
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 403)

    def test_vehicle_create_unauthenticated(self):
        self.client.credentials()
        data = self.vehicle_data.copy()
        data['license_plate'] = 'PLT-NEW3'
        data['vin'] = 'VIN-JWT-NEW3'
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 401)

    def test_vehicle_create_invalid_payload(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {'brand': 'TestBrand'}  # Missing required fields
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, 400)

    def test_vehicle_detail_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.detail_url())
        self.assertEqual(response.status_code, 200)

    def test_vehicle_detail_non_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_driver_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.detail_url())
        self.assertEqual(response.status_code, 403)

    def test_vehicle_detail_unauthenticated(self):
        self.client.credentials()
        response = self.client.get(self.detail_url())
        self.assertEqual(response.status_code, 401)

    def test_vehicle_detail_not_found(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('CarFleetManagement.api:api-vehicle-detail', args=[99999])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_vehicle_update_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = self.vehicle_data.copy()
        data['brand'] = 'UpdatedBrand'
        response = self.client.put(self.detail_url(), data)
        self.assertEqual(response.status_code, 200)
        self.vehicle.refresh_from_db()
        self.assertEqual(self.vehicle.brand, 'UpdatedBrand')

    def test_vehicle_update_non_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_driver_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = self.vehicle_data.copy()
        data['brand'] = 'ShouldNotUpdate'
        response = self.client.put(self.detail_url(), data)
        self.assertEqual(response.status_code, 403)

    def test_vehicle_update_unauthenticated(self):
        self.client.credentials()
        data = self.vehicle_data.copy()
        data['brand'] = 'ShouldNotUpdate'
        response = self.client.put(self.detail_url(), data)
        self.assertEqual(response.status_code, 401)

    def test_vehicle_update_not_found(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = self.vehicle_data.copy()
        data['brand'] = 'ShouldNotUpdate'
        url = reverse('CarFleetManagement.api:api-vehicle-detail', args=[99999])
        response = self.client.put(url, data)
        self.assertEqual(response.status_code, 404)

    def test_vehicle_delete_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.detail_url())
        self.assertEqual(response.status_code, 204)

    def test_vehicle_delete_non_admin_jwt(self):
        token = self.get_jwt_token(self.jwt_driver_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(self.detail_url())
        self.assertEqual(response.status_code, 403)

    def test_vehicle_delete_unauthenticated(self):
        self.client.credentials()
        response = self.client.delete(self.detail_url())
        self.assertEqual(response.status_code, 401)

    def test_vehicle_delete_not_found(self):
        token = self.get_jwt_token(self.jwt_admin_user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = reverse('CarFleetManagement.api:api-vehicle-detail', args=[99999])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404)