import os
from django.conf import settings
from api.openrouter_client import OpenRouterClient
from api.gemini_client import GeminiClient

def test_both_clients():
    # Initialize both clients
    openrouter_client = OpenRouterClient()
    gemini_client = GeminiClient()
    
    # Get a test screenshot from debug_screenshots directory
    screenshot_path = os.path.join(settings.BASE_DIR, 'debug_screenshots', 'home_en_dark_20250331-201208.png')
    
    if not os.path.exists(screenshot_path):
        print(f"Screenshot not found at {screenshot_path}")
        return
    
    # Test OpenRouter analysis
    print("\nTesting OpenRouter Analysis:")
    print("-" * 50)
    try:
        openrouter_result = openrouter_client.analyze_screenshot(screenshot_path)
        print("OpenRouter Analysis Result:")
        print(openrouter_result)
    except Exception as e:
        print(f"OpenRouter Analysis Error: {str(e)}")
    
    # Test Gemini analysis
    print("\nTesting Gemini Analysis:")
    print("-" * 50)
    try:
        gemini_result = gemini_client.analyze_screenshot(screenshot_path)
        print("Gemini Analysis Result:")
        print(gemini_result)
    except Exception as e:
        print(f"Gemini Analysis Error: {str(e)}")

if __name__ == '__main__':
    test_both_clients()