"""Management command to capture debug screenshots of the application.

This command uses Selenium to open the application in different languages and themes,
capturing screenshots for debugging UI issues.
"""

import os
import time
import socket
import subprocess
import sys
import threading
from django.core.management.base import BaseCommand
from django.conf import settings
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import urlparse

from car_fleet_manager.utils import toggle_screenshot_debug, capture_screenshot

class Command(BaseCommand):
    help = 'Capture screenshots of the application in different languages and themes for debugging'
    
    def add_arguments(self, parser):
        parser.add_argument(
            '--url', 
            default='http://localhost:8000',
            help='Base URL of the application'
        )
        parser.add_argument(
            '--pages',
            nargs='+',
            default=['/', '/about/', '/features/'],
            help='List of page paths to capture'
        )
        parser.add_argument(
            '--output-dir',
            default=None,
            help='Directory to save screenshots (defaults to debug_screenshots in BASE_DIR)'
        )
        parser.add_argument(
            '--start-server',
            action='store_true',
            help='Start the Django development server if not running'
        )
        parser.add_argument(
            '--server-wait',
            type=int,
            default=5,
            help='Time to wait for server to start (in seconds)'
        )
        parser.add_argument(
            '--retry-count',
            type=int,
            default=3,
            help='Number of times to retry connecting to the server'
        )
        parser.add_argument(
            '--retry-delay',
            type=int,
            default=2,
            help='Delay between retries (in seconds)'
        )
        
    def is_server_running(self, url):
        """Check if the server is running at the given URL."""
        parsed_url = urlparse(url)
        host = parsed_url.hostname
        port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
        
        try:
            # Try to connect to the server
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(1)
                s.connect((host, port))
                return True
        except (socket.timeout, socket.error, ConnectionRefusedError):
            return False
    
    def start_django_server(self, host='127.0.0.1', port=8000):
        """Start the Django development server in a separate thread."""
        self.stdout.write(self.style.WARNING(f"Starting Django development server at {host}:{port}..."))
        
        # Determine the path to manage.py
        manage_py = os.path.join(settings.BASE_DIR, 'manage.py')
        if not os.path.exists(manage_py):
            # Try to find manage.py in parent directory
            manage_py = os.path.join(os.path.dirname(settings.BASE_DIR), 'manage.py')
        
        if not os.path.exists(manage_py):
            self.stdout.write(self.style.ERROR(f"Could not find manage.py in {settings.BASE_DIR} or its parent directory"))
            return False
        
        # Start the server in a separate process
        cmd = [sys.executable, manage_py, 'runserver', f"{host}:{port}"]
        try:
            process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            self.server_process = process
            return True
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error starting Django server: {e}"))
            return False
    
    def handle(self, *args, **options):
        # Enable screenshot debugging
        toggle_screenshot_debug(True)
        
        base_url = options['url']
        pages = options['pages']
        start_server = options['start_server']
        server_wait = options['server_wait']
        retry_count = options['retry_count']
        retry_delay = options['retry_delay']
        
        # Set up output directory
        output_dir = options['output_dir'] or os.path.join(settings.BASE_DIR, 'debug_screenshots')
        os.makedirs(output_dir, exist_ok=True)
        
        # Check if the server is running
        server_running = self.is_server_running(base_url)
        self.server_process = None
        
        if not server_running:
            self.stdout.write(self.style.WARNING(f"Server not running at {base_url}"))
            
            if start_server:
                # Parse URL to get host and port
                parsed_url = urlparse(base_url)
                host = parsed_url.hostname or '127.0.0.1'
                port = parsed_url.port or (443 if parsed_url.scheme == 'https' else 80)
                
                # Start the server
                if self.start_django_server(host, port):
                    self.stdout.write(self.style.SUCCESS(f"Django server started. Waiting {server_wait} seconds for it to initialize..."))
                    time.sleep(server_wait)
                else:
                    self.stdout.write(self.style.ERROR("Failed to start Django server. Please start it manually."))
                    return
            else:
                self.stdout.write(self.style.ERROR(
                    "Server not running. Please start the Django development server first or use --start-server option."
                ))
                return
        
        # Configure Chrome options
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--window-size=1920,1080')  # Set window size
        
        # Available languages and themes
        languages = [lang_code for lang_code, _ in settings.LANGUAGES]
        themes = ['light', 'dark']
        
        try:
            # Initialize the WebDriver
            driver = webdriver.Chrome(options=chrome_options)
            
            # Capture screenshots for each combination
            for lang in languages:
                for theme in themes:
                    for page_path in pages:
                        # Construct the full URL
                        url = f"{base_url}{page_path}"
                        
                        # Navigate to the page
                        self.stdout.write(f"Navigating to {url} with language={lang}, theme={theme}")
                        driver.get(url)
                        
                        # Wait for page to load
                        WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.TAG_NAME, "body"))
                        )
                        
                        # Set language if not already set
                        current_lang = driver.execute_script(
                            "return document.documentElement.lang;"
                        )
                        if current_lang != lang:
                            # Click language selector and select language
                            try:
                                # Open language selector
                                selector = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.ID, "language-selector"))
                                )
                                selector.click()
                                
                                # Select the language option
                                driver.execute_script(
                                    f"document.getElementById('language-selector').value = '{lang}';"
                                    f"document.getElementById('language-selector').dispatchEvent(new Event('change'));"
                                )
                                
                                # Wait for page to reload
                                time.sleep(3)
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Error setting language: {e}"))
                        
                        # Set theme if not already set
                        current_theme = driver.execute_script(
                            "return document.documentElement.getAttribute('data-theme') || 'light';"
                        )
                        if current_theme != theme:
                            try:
                                # Toggle theme checkbox
                                checkbox = WebDriverWait(driver, 5).until(
                                    EC.element_to_be_clickable((By.ID, "theme-toggle-checkbox"))
                                )
                                checkbox.click()
                                
                                # Wait for theme to apply
                                time.sleep(1)
                            except Exception as e:
                                self.stdout.write(self.style.WARNING(f"Error setting theme: {e}"))
                        
                        # Capture screenshot
                        page_name = page_path.strip('/').replace('/', '_') or 'home'
                        screenshot_name = f"{page_name}_{lang}_{theme}"
                        screenshot_path = capture_screenshot(driver, screenshot_name)
                        
                        self.stdout.write(
                            self.style.SUCCESS(f"Captured screenshot: {screenshot_path}")
                        )
                        
                        # Small delay between pages
                        time.sleep(1)
            
            self.stdout.write(self.style.SUCCESS("All screenshots captured successfully"))
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error capturing screenshots: {e}"))
            
            # If it's a connection error, provide more helpful information
            if "ERR_CONNECTION_REFUSED" in str(e):
                self.stdout.write(self.style.WARNING("\nConnection refused error detected. Possible solutions:"))
                self.stdout.write("1. Make sure the Django server is running at the specified URL")
                self.stdout.write("2. Use --start-server option to automatically start the server")
                self.stdout.write("3. Check if the port is correct and not blocked by a firewall")
                self.stdout.write("4. Verify that no other service is using the same port")
                
                # Try to reconnect a few times
                if retry_count > 0:
                    self.stdout.write(self.style.WARNING(f"\nRetrying connection {retry_count} times..."))
                    for i in range(retry_count):
                        self.stdout.write(f"Retry attempt {i+1}/{retry_count}...")
                        time.sleep(retry_delay)
                        
                        if self.is_server_running(base_url):
                            self.stdout.write(self.style.SUCCESS("Server is now available! Try running the command again."))
                            break
                    else:
                        self.stdout.write(self.style.ERROR("All retry attempts failed."))
        
        finally:
            # Clean up
            if 'driver' in locals():
                driver.quit()
            
            # Terminate the server process if we started it
            if self.server_process:
                self.stdout.write("Shutting down Django server...")
                self.server_process.terminate()
                self.server_process.wait()
            
            # Disable screenshot debugging
            toggle_screenshot_debug(False)