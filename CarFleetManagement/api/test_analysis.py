import os
import pytest
from unittest.mock import patch, MagicMock
from django.conf import settings
from CarFleetManagement.api.openrouter_client import OpenRouterClient  # Ensure this is the client intended to be instantiated
from CarFleetManagement.api.gemini_client import GeminiClient      # Ensure this is the client intended to be instantiated

@patch('CarFleetManagement.api.gemini_client.GeminiClient')
@patch('CarFleetManagement.api.openrouter_client.OpenRouterClient')
def test_api_clients_analyze_screenshots_mocked(MockOpenRouterClient, MockGeminiClient):
    """Tests client analysis methods with GeminiClient and OpenRouterClient mocked."""
    # Configure the mock instances that the constructors will return
    mock_openrouter_instance = MockOpenRouterClient.return_value
    mock_gemini_instance = MockGeminiClient.return_value

    # Configure the return value of the analyze_screenshot method on these mock instances
    mock_openrouter_instance.analyze_screenshot.return_value = {"status": "success", "client": "openrouter_mock"}
    mock_gemini_instance.analyze_screenshot.return_value = {"status": "success", "client": "gemini_mock"}

    # Instantiate the clients. Due to patching, these will be the mock classes,
    # and will return the configured mock_instances.
    # The original __init__ methods (checking for API keys) will not be called.
    openrouter_client = OpenRouterClient() 
    gemini_client = GeminiClient()

    assert openrouter_client is mock_openrouter_instance
    assert gemini_client is mock_gemini_instance
    
    screenshot_filename = 'home_en_dark_20250331-201208.png' # Example file
    screenshot_path = os.path.join(settings.BASE_DIR, 'debug_screenshots', screenshot_filename)
    
    # Create a dummy screenshot file if it doesn't exist, to prevent FileNotFoundError
    # In a real CI environment, test assets should be committed or generated reliably.
    if not os.path.exists(screenshot_path):
        os.makedirs(os.path.dirname(screenshot_path), exist_ok=True)
        with open(screenshot_path, 'w') as f:
            f.write("dummy screenshot content") # Minimal content for the file to exist
        # Consider pytest.skip if the file truly cannot be made available for the test
        # pytest.skip(f"Test screenshot {screenshot_filename} not found and could not be created.")

    # Test OpenRouter analysis
    openrouter_result = openrouter_client.analyze_screenshot(screenshot_path)
    assert openrouter_result == {"status": "success", "client": "openrouter_mock"}
    mock_openrouter_instance.analyze_screenshot.assert_called_once_with(screenshot_path)
    
    # Test Gemini analysis
    gemini_result = gemini_client.analyze_screenshot(screenshot_path)
    assert gemini_result == {"status": "success", "client": "gemini_mock"}
    mock_gemini_instance.analyze_screenshot.assert_called_once_with(screenshot_path)