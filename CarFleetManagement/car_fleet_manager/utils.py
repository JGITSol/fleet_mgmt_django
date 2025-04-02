"""Utility functions for the car fleet manager application.

This module contains utility functions used across the application,
including debugging and screenshot capture utilities.
"""

import os
import time
from django.conf import settings

# Global variable to track if screenshot debugging is enabled
_screenshot_debug_enabled = False

def toggle_screenshot_debug(enable):
    """Enable or disable screenshot debugging mode.
    
    Args:
        enable (bool): True to enable screenshot debugging, False to disable
    
    Returns:
        bool: The new state of screenshot debugging
    """
    global _screenshot_debug_enabled
    _screenshot_debug_enabled = enable
    return _screenshot_debug_enabled

def is_screenshot_debug_enabled():
    """Check if screenshot debugging is enabled.
    
    Returns:
        bool: True if screenshot debugging is enabled, False otherwise
    """
    return _screenshot_debug_enabled

def capture_screenshot(driver, screenshot_name):
    """Capture a screenshot using Selenium WebDriver.
    
    Args:
        driver (selenium.webdriver.Chrome): The Selenium WebDriver instance
        screenshot_name (str): The name to use for the screenshot file
    
    Returns:
        str: The path to the saved screenshot file
    """
    # Only capture screenshots if debugging is enabled
    if not is_screenshot_debug_enabled():
        return None
    
    # Set up output directory
    output_dir = os.path.join(settings.BASE_DIR, 'debug_screenshots')
    os.makedirs(output_dir, exist_ok=True)
    
    # Generate a unique filename with timestamp
    timestamp = time.strftime("%Y%m%d-%H%M%S")
    filename = f"{screenshot_name}_{timestamp}.png"
    screenshot_path = os.path.join(output_dir, filename)
    
    # Capture the screenshot
    driver.save_screenshot(screenshot_path)
    
    return screenshot_path