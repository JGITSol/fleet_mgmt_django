import os
import json
from unittest import mock
from django.test import TestCase
from django.urls import reverse
from django.conf import settings
from rest_framework.test import APIClient
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile


class AnalyzeScreenshotViewTestCase(TestCase):
    """Test cases for the AnalyzeScreenshotView."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.url = reverse('analyze_screenshot')
        
        # Create a test image file
        self.image_content = b'test image content'
        self.test_image = SimpleUploadedFile(
            name='test_screenshot.png',
            content=self.image_content,
            content_type='image/png'
        )
    
    def tearDown(self):
        """Clean up test environment."""
        # Ensure temp directory is cleaned up
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_screenshots')
        if os.path.exists(temp_dir):
            for file in os.listdir(temp_dir):
                os.remove(os.path.join(temp_dir, file))
            if os.path.exists(temp_dir):
                os.rmdir(temp_dir)
    
    def test_post_without_screenshot(self):
        """Test POST request without screenshot file."""
        response = self.client.post(self.url, {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('error', response.data)
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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


class BatchAnalyzeScreenshotsViewTestCase(TestCase):
    """Test cases for the BatchAnalyzeScreenshotsView."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.url = reverse('batch_analyze_screenshots')
        
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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
    
    @mock.patch('api.views.get_client')
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


class GenerateReportViewTestCase(TestCase):
    """Test cases for the GenerateReportView."""
    
    def setUp(self):
        """Set up test environment."""
        self.client = APIClient()
        self.url = reverse('generate_report')
        
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
    
    @mock.patch('api.views.generate_report')
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
    
    @mock.patch('api.views.generate_report')
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