import os
from unittest import mock

from django.conf import settings
from rest_framework.test import APITestCase

from CarFleetManagement.api.openrouter_client import OpenRouterClient, get_client


class OpenRouterClientTestCase(APITestCase):
    """Test cases for the OpenRouterClient class."""

    def setUp(self):
        """Set up test environment."""
        self.api_key = 'test_api_key'
        self.client = OpenRouterClient(api_key=self.api_key)

        # Create a test screenshot directory
        self.test_dir = os.path.join(settings.BASE_DIR, 'test_screenshots')
        os.makedirs(self.test_dir, exist_ok=True)

        # Create a valid PNG image as the test screenshot file
        from PIL import Image
        self.test_screenshot = os.path.join(self.test_dir, 'home_en_dark_20250331-201208.png')
        img = Image.new('RGB', (100, 100), color = (73, 109, 137))
        img.save(self.test_screenshot, 'PNG')

    def tearDown(self):
        """Clean up test environment."""
        # Remove all files in the test directory
        if os.path.exists(self.test_dir):
            for filename in os.listdir(self.test_dir):
                file_path = os.path.join(self.test_dir, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        import shutil
                        shutil.rmtree(file_path)
                except Exception:
                    pass
            try:
                os.rmdir(self.test_dir)
            except Exception:
                pass

    def test_init_with_api_key(self):
        """Test initialization with API key."""
        self.assertEqual(self.client.api_key, self.api_key)

    @mock.patch('api.openrouter_client.OPENROUTER_API_KEY', 'env_api_key')
    def test_init_without_api_key(self):
        """Test initialization without API key (using environment variable)."""
        client = OpenRouterClient()
        self.assertEqual(client.api_key, 'env_api_key')

    @mock.patch('api.openrouter_client.OPENROUTER_API_KEY', None)
    def test_init_without_api_key_and_env(self):
        """Test initialization without API key and environment variable."""
        with self.assertRaises(ValueError):
            OpenRouterClient()

    def test_analyze_screenshot_file_not_found(self):
        """Test analyze_screenshot with non-existent file."""
        with self.assertRaises(FileNotFoundError):
            self.client.analyze_screenshot('nonexistent_file.png')

    @mock.patch('requests.post')
    def test_analyze_screenshot_success(self, mock_post):
        """Test analyze_screenshot with successful API response."""
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.json.return_value = {
            'choices': [
                {
                    'message': {
                        'content': 'Analysis result'
                    }
                }
            ]
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Call the method
        result = self.client.analyze_screenshot(self.test_screenshot)

        # Verify the result
        self.assertEqual(result, mock_response.json.return_value)

        # Verify the API call
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertIn('openrouter.ai/api/v1/chat/completions', args[0])
        self.assertEqual(kwargs['headers']['Authorization'], f'Bearer {self.api_key}')

    @mock.patch('requests.post')
    def test_analyze_screenshot_with_custom_prompt(self, mock_post):
        """Test analyze_screenshot with custom prompt."""
        # Mock the API response
        mock_response = mock.Mock()
        mock_response.json.return_value = {'choices': [{'message': {'content': 'Analysis result'}}]}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        # Call the method with custom prompt
        custom_prompt = 'Custom analysis prompt'
        result = self.client.analyze_screenshot(self.test_screenshot, prompt=custom_prompt)

        # Verify the prompt was used
        args, kwargs = mock_post.call_args
        # Check that the custom prompt is in the text field of the first content item
        self.assertEqual(custom_prompt, kwargs['json']['messages'][0]['content'][0]['text'])

    @mock.patch('requests.post')
    def test_analyze_screenshot_api_error(self, mock_post):
        """Test analyze_screenshot with API error."""
        # Mock the API error
        mock_post.side_effect = Exception('API error')

        # Call the method
        result = self.client.analyze_screenshot(self.test_screenshot)

        # Verify the error is handled
        self.assertEqual(result, {'error': 'API error'})

    def test_batch_analyze_screenshots_directory_not_found(self):
        """Test batch_analyze_screenshots with non-existent directory."""
        with self.assertRaises(NotADirectoryError):
            self.client.batch_analyze_screenshots('nonexistent_dir')

    @mock.patch('api.openrouter_client.OpenRouterClient.analyze_screenshot')
    def test_batch_analyze_screenshots(self, mock_analyze):
        """Test batch_analyze_screenshots."""
        # Mock the analyze_screenshot method
        mock_analyze.return_value = {'choices': [{'message': {'content': 'Analysis result'}}]}

        # Call the method
        result = self.client.batch_analyze_screenshots(self.test_dir)

        # Verify the result
        self.assertIn('home_en_dark_20250331-201208.png', result)
        self.assertEqual(result['home_en_dark_20250331-201208.png'], mock_analyze.return_value)

        # Verify analyze_screenshot was called
        mock_analyze.assert_called_once_with(self.test_screenshot)

    @mock.patch('api.openrouter_client.OpenRouterClient.analyze_screenshot')
    def test_batch_analyze_screenshots_with_filters(self, mock_analyze):
        """Test batch_analyze_screenshots with language and theme filters."""
        # Create additional test screenshots
        test_screenshot2 = os.path.join(self.test_dir, 'home_fr_dark_20250331-201238.png')
        test_screenshot3 = os.path.join(self.test_dir, 'home_en_light_20250331-201203.png')

        with open(test_screenshot2, 'w') as f:
            f.write('test image content')
        with open(test_screenshot3, 'w') as f:
            f.write('test image content')

        # Mock the analyze_screenshot method
        mock_analyze.return_value = {'choices': [{'message': {'content': 'Analysis result'}}]}

        # Test with language filter
        result = self.client.batch_analyze_screenshots(self.test_dir, language='en')
        self.assertEqual(len(result), 2)  # Should include both en screenshots
        self.assertIn('home_en_dark_20250331-201208.png', result)
        self.assertIn('home_en_light_20250331-201203.png', result)

        # Test with theme filter
        result = self.client.batch_analyze_screenshots(self.test_dir, theme='dark')
        self.assertEqual(len(result), 2)  # Should include both dark screenshots
        self.assertIn('home_en_dark_20250331-201208.png', result)
        self.assertIn('home_fr_dark_20250331-201238.png', result)

        # Test with both filters
        result = self.client.batch_analyze_screenshots(self.test_dir, language='en', theme='dark')
        self.assertEqual(len(result), 1)  # Should include only the en+dark screenshot
        self.assertIn('home_en_dark_20250331-201208.png', result)

        # Clean up additional test files
        if os.path.exists(test_screenshot2):
            os.remove(test_screenshot2)
        if os.path.exists(test_screenshot3):
            os.remove(test_screenshot3)

    def test_get_client(self):
        """Test get_client function."""
        with mock.patch('api.openrouter_client.OpenRouterClient') as mock_client:
            client = get_client()
            mock_client.assert_called_once()
            self.assertEqual(client, mock_client.return_value)
