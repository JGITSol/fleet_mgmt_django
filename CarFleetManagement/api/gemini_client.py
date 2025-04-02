"""Gemini API client for the Car Fleet Management system.

This module provides functionality to interact with the Google Gemini API
for AI-powered analysis of screenshots and other data.
"""

import os
import base64
import time
import requests
from io import BytesIO
from pathlib import Path
from PIL import Image
from dotenv import load_dotenv
from django.conf import settings
import google.generativeai as genai

# Load environment variables from .env file
env_path = Path(settings.BASE_DIR) / '.env'
load_dotenv(dotenv_path=env_path)

# Get API key from environment variables
GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')

# Constants for rate limiting and image processing
MAX_REQUESTS_PER_MINUTE = 10  # Adjust based on Gemini API limits
REQUEST_INTERVAL = 60 / MAX_REQUESTS_PER_MINUTE  # Time between requests in seconds
MAX_IMAGE_RESOLUTION = (1920, 1080)  # FullHD resolution

class GeminiClient:
    """Client for interacting with the Google Gemini API."""
    
    def __init__(self, api_key=None):
        """Initialize the Gemini client.
        
        Args:
            api_key (str, optional): API key for Gemini. Defaults to the one in .env file.
        """
        self.api_key = api_key or GEMINI_API_KEY
        if not self.api_key:
            raise ValueError("Gemini API key is not set. Please add GEMINI_API_KEY to your .env file.")
        
        # Initialize Gemini client
        genai.configure(api_key=self.api_key)
        
        # Rate limiting attributes
        self.last_request_time = 0
    
    def _resize_image(self, image_path):
        """Resize image to FullHD resolution if larger.
        
        Args:
            image_path (str): Path to the image file
            
        Returns:
            BytesIO: BytesIO object containing the resized image
        """
        with Image.open(image_path) as img:
            # Check if resizing is needed
            if img.width > MAX_IMAGE_RESOLUTION[0] or img.height > MAX_IMAGE_RESOLUTION[1]:
                img.thumbnail(MAX_IMAGE_RESOLUTION, Image.LANCZOS)
            
            # Save to BytesIO
            img_byte_arr = BytesIO()
            img_format = img.format if img.format else 'PNG'
            img.save(img_byte_arr, format=img_format)
            img_byte_arr.seek(0)
            
            return img_byte_arr
    
    def _apply_rate_limit(self):
        """Apply rate limiting to avoid hitting API limits."""
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        
        if time_since_last_request < REQUEST_INTERVAL:
            sleep_time = REQUEST_INTERVAL - time_since_last_request
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def analyze_screenshot(self, screenshot_path, prompt=None):
        """Analyze a screenshot using Gemini's vision capabilities.
        
        Args:
            screenshot_path (str): Path to the screenshot file
            prompt (str, optional): Custom prompt to guide the analysis
            
        Returns:
            dict: The analysis results from Gemini
        """
        if not os.path.exists(screenshot_path):
            raise FileNotFoundError(f"Screenshot not found at {screenshot_path}")
        
        # Default prompt if none provided
        if not prompt:
            prompt = "Analyze this UI screenshot focusing on UI/UX aspects: "\
                    "1. Theme consistency and color contrast ratios "\
                    "2. Text readability and font rendering "\
                    "3. Layout spacing and alignment "\
                    "4. Accessibility concerns "\
                    "5. Visual hierarchy and element relationships"
        
        try:
            # Apply rate limiting
            self._apply_rate_limit()
            
            # Resize image if needed
            img_data = self._resize_image(screenshot_path)
            
            # Get Gemini model
            model = genai.GenerativeModel('gemini-2.0-flash')
            
            # Prepare image for the model
            image_parts = [
                {"mime_type": "image/png", "data": base64.b64encode(img_data.getvalue()).decode('utf-8')}
            ]
            
            # Generate response
            response = model.generate_content(
                contents=[
                    prompt,
                    image_parts[0]
                ]
            )
            
            # Format response to match OpenRouter format for compatibility
            formatted_response = {
                "choices": [
                    {
                        "message": {
                            "content": response.text,
                            "role": "assistant"
                        }
                    }
                ]
            }
            
            return formatted_response
        except Exception as e:
            return {"error": str(e)}
    
    def batch_analyze_screenshots(self, screenshot_dir, language=None, theme=None):
        """Analyze multiple screenshots in a directory.
        
        Args:
            screenshot_dir (str): Directory containing screenshots
            language (str, optional): Filter screenshots by language
            theme (str, optional): Filter screenshots by theme (light/dark)
            
        Returns:
            dict: Analysis results for each screenshot
        """
        results = {}
        
        if not os.path.isdir(screenshot_dir):
            raise NotADirectoryError(f"{screenshot_dir} is not a valid directory")
        
        # Get all PNG files in the directory
        screenshots = [f for f in os.listdir(screenshot_dir) if f.endswith('.png')]
        
        # Apply filters if specified
        if language:
            screenshots = [s for s in screenshots if f"_{language}_" in s]
        if theme:
            screenshots = [s for s in screenshots if f"_{theme}_" in s]
        
        for screenshot in screenshots:
            screenshot_path = os.path.join(screenshot_dir, screenshot)
            results[screenshot] = self.analyze_screenshot(screenshot_path)
        
        return results


def get_client():
    """Get an initialized Gemini client.
    
    Returns:
        GeminiClient: An initialized client instance
    """
    return GeminiClient()