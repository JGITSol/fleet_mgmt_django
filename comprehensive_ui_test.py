#!/usr/bin/env python3
"""
Comprehensive UI Testing Script for Car Fleet Management System

This script performs complete testing of the user interface including:
- URL accessibility testing
- Screenshot capture for visual verification
- Form testing
- Authentication flow testing
- API endpoint testing
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import requests

# Add Django project to Python path
project_root = Path(__file__).parent / "CarFleetManagement"
sys.path.insert(0, str(project_root))

# Set Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")



import django
from conftest import TEST_PASSWORD


class ComprehensiveUITester:
    def __init__(self):
        # Configure Django at runtime; caller is responsible for calling
        # django.setup() before constructing this class when used as a
        # library. When executed as a script we call setup() in main().
        from django.contrib.auth import get_user_model
        from django.test import Client

        self.base_url = "http://localhost:8000"
        self.client = Client()
        self.session = requests.Session()
        self.User = get_user_model()
        self.test_results = []
        self.screenshot_dir = Path("ui_test_screenshots")
        self.screenshot_dir.mkdir(exist_ok=True)
        self.log_file = Path("ui_test_log.txt")

    def log(self, message, level="INFO"):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        print(log_entry)

        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(log_entry + "\n")

    def setup_test_data(self):
        """Create test data for comprehensive testing"""
        self.log("Setting up test data...")

        # Create test user if not exists
        try:
            self.test_user = self.User.objects.get(username="testuser")
            self.log("Test user already exists")
        except User.DoesNotExist:
            self.test_user = self.User.objects.create_user(
                username="testuser",
                email="test@example.com",
                password=TEST_PASSWORD,
                first_name="Test",
                last_name="User",
            )
            self.log("Created test user")

        # Create admin user if not exists
        try:
            self.admin_user = self.User.objects.get(username="admin", is_superuser=True)
            self.log("Admin user already exists")
        except User.DoesNotExist:
            self.admin_user = self.User.objects.create_superuser(
                username="admin", email="admin@example.com", password=TEST_PASSWORD
            )
            self.log("Created admin user")

    def test_url_accessibility(self):
        """Test all URL patterns for accessibility"""
        self.log("Testing URL accessibility...")

        # Define URLs to test
        urls_to_test = [
            # Public URLs
            ("/", "Home Page"),
            ("/admin/", "Admin Login"),
            ("/api/", "API Root"),
            # Authentication URLs
            ("/accounts/login/", "Login Page"),
            ("/accounts/register/", "Register Page"),
            # Main app URLs (may require auth)
            ("/vehicles/", "Vehicle List"),
            ("/maintenance/", "Maintenance List"),
            ("/emergency/", "Emergency List"),
            # API endpoints
            ("/api/vehicles/", "API Vehicles"),
            ("/api/drivers/", "API Drivers"),
            ("/api/maintenance/", "API Maintenance"),
            ("/api/emergencies/", "API Emergencies"),
        ]

        results = []
        for url, description in urls_to_test:
            try:
                response = self.session.get(f"{self.base_url}{url}", timeout=10)
                status = (
                    "✓ PASS"
                    if response.status_code < 400
                    else f"✗ FAIL ({response.status_code})"
                )
                self.log(f"{status} - {description}: {url}")
                results.append(
                    {
                        "url": url,
                        "description": description,
                        "status_code": response.status_code,
                        "success": response.status_code < 400,
                    }
                )
            except Exception as e:
                self.log(f"✗ ERROR - {description}: {url} - {str(e)}", "ERROR")
                results.append(
                    {
                        "url": url,
                        "description": description,
                        "status_code": None,
                        "success": False,
                        "error": str(e),
                    }
                )

        return results

    def test_authentication_flow(self):
        """Test authentication functionality"""
        self.log("Testing authentication flow...")

        # Test login
        login_data = {"username": "testuser", "password": "testpass123"}

        try:
            response = self.session.post(
                f"{self.base_url}/accounts/login/", data=login_data
            )
            if response.status_code == 200 or response.status_code == 302:
                self.log("✓ Login test passed")
                return True
            else:
                self.log(f"✗ Login test failed: {response.status_code}")
                return False
        except Exception as e:
            self.log(f"✗ Login test error: {str(e)}", "ERROR")
            return False

    def test_api_endpoints(self):
        """Test API endpoints functionality"""
        self.log("Testing API endpoints...")

        # First try to get JWT token
        jwt_token = None
        try:
            auth_response = self.session.post(
                f"{self.base_url}/api/auth/login/",
                json={"username": "testuser", "password": "testpass123"},
            )
            if auth_response.status_code == 200:
                jwt_token = auth_response.json().get("access")
                self.log("✓ JWT authentication successful")
            else:
                self.log("⚠ JWT authentication failed, testing without auth")
        except Exception as e:
            self.log(f"⚠ JWT auth error: {str(e)}")

        # Test API endpoints
        api_endpoints = [
            "/api/",
            "/api/vehicles/",
            "/api/drivers/",
            "/api/maintenance/",
            "/api/emergencies/",
        ]

        headers = {}
        if jwt_token:
            headers["Authorization"] = f"Bearer {jwt_token}"

        results = []
        for endpoint in api_endpoints:
            try:
                response = self.session.get(
                    f"{self.base_url}{endpoint}", headers=headers
                )
                status = (
                    "✓ PASS"
                    if response.status_code < 400
                    else f"✗ FAIL ({response.status_code})"
                )
                self.log(f"{status} - API {endpoint}")
                results.append(
                    {
                        "endpoint": endpoint,
                        "status_code": response.status_code,
                        "success": response.status_code < 400,
                    }
                )
            except Exception as e:
                self.log(f"✗ ERROR - API {endpoint}: {str(e)}", "ERROR")
                results.append(
                    {"endpoint": endpoint, "success": False, "error": str(e)}
                )

        return results

    def capture_screenshots_with_puppeteer(self):
        """Capture screenshots using Puppeteer if available"""
        self.log("Attempting to capture screenshots with Puppeteer...")

        # Create a simple Node.js script for Puppeteer
        puppeteer_script = """
const puppeteer = require('puppeteer');
const fs = require('fs');

(async () => {
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  const urls = [
    { url: 'http://localhost:8000/', name: 'home' },
    { url: 'http://localhost:8000/api/', name: 'api_root' },
    { url: 'http://localhost:8000/admin/', name: 'admin_login' },
    { url: 'http://localhost:8000/accounts/login/', name: 'login_page' },
    { url: 'http://localhost:8000/vehicles/', name: 'vehicles_list' },
    { url: 'http://localhost:8000/maintenance/', name: 'maintenance_list' },
    { url: 'http://localhost:8000/emergency/', name: 'emergency_list' }
  ];
  
  for (const item of urls) {
    try {
      await page.goto(item.url, { waitUntil: 'networkidle2', timeout: 10000 });
      await page.screenshot({ 
        path: `ui_test_screenshots/${item.name}.png`,
        fullPage: true 
      });
      console.log(`✓ Screenshot captured: ${item.name}.png`);
    } catch (error) {
      console.log(`✗ Failed to capture ${item.name}: ${error.message}`);
    }
  }
  
  await browser.close();
})();
"""

        # Write the script to a temporary file
        script_path = Path("temp_puppeteer_script.js")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(puppeteer_script)

        try:
            # Check if Node.js and Puppeteer are available
            result = subprocess.run(  # noqa: S603
                ["node", "--version"], capture_output=True, text=True, timeout=5
            )

            if result.returncode == 0:
                self.log(f"Node.js version: {result.stdout.strip()}")

                # Try to run the Puppeteer script
                result = subprocess.run(  # noqa: S603
                    ["node", str(script_path)],
                    capture_output=True,
                    text=True,
                    timeout=60,
                )

                if result.returncode == 0:
                    self.log("✓ Puppeteer screenshots captured successfully")
                    self.log(result.stdout)
                    return True
                else:
                    self.log(f"⚠ Puppeteer failed: {result.stderr}")
                    return False
            else:
                self.log("⚠ Node.js not available, skipping Puppeteer screenshots")
                return False

        except subprocess.TimeoutExpired:
            self.log("⚠ Puppeteer script timed out")
            return False
        except FileNotFoundError:
            self.log("⚠ Node.js not found, skipping Puppeteer screenshots")
            return False
        except Exception as e:
            self.log(f"⚠ Puppeteer error: {str(e)}")
            return False
        finally:
            # Clean up temporary script
            if script_path.exists():
                script_path.unlink()

    def run_django_tests(self):
        """Run Django test suite"""
        self.log("Running Django test suite...")

        try:
            # Change to the Django project directory
            original_cwd = os.getcwd()
            os.chdir("CarFleetManagement")

            # Run tests with coverage
            result = subprocess.run(  # noqa: S603
                [sys.executable, "manage.py", "test", "--verbosity=2"],
                capture_output=True,
                text=True,
                timeout=300,  # 5 minutes timeout
            )

            self.log(f"Django tests exit code: {result.returncode}")
            if result.stdout:
                self.log("Test output:")
                self.log(result.stdout)
            if result.stderr:
                self.log("Test errors:")
                self.log(result.stderr)

            return result.returncode == 0

        except subprocess.TimeoutExpired:
            self.log("Django tests timed out", "ERROR")
            return False
        except Exception as e:
            self.log(f"Error running Django tests: {str(e)}", "ERROR")
            return False
        finally:
            os.chdir(original_cwd)

    def check_server_status(self):
        """Check if Django server is running"""
        try:
            response = requests.get(self.base_url, timeout=5)
            if response.status_code == 200:
                self.log("✓ Django server is running")
                return True
            else:
                self.log(f"⚠ Django server returned status {response.status_code}")
                return False
        except requests.exceptions.ConnectionError:
            self.log("✗ Django server is not running")
            return False
        except Exception as e:
            self.log(f"✗ Error checking server: {str(e)}")
            return False

    def generate_report(self, results):
        """Generate comprehensive test report"""
        self.log("Generating test report...")

        report_path = Path("ui_test_report.html")

        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Fleet Management UI Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .success {{ color: #27ae60; }}
        .error {{ color: #e74c3c; }}
        .warning {{ color: #f39c12; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
        th {{ background-color: #f2f2f2; }}
        .screenshot {{ max-width: 300px; margin: 10px; border: 1px solid #ddd; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>Car Fleet Management System - UI Test Report</h1>
        <p>Generated on: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
    </div>
    
    <div class="section">
        <h2>Test Summary</h2>
        <p><strong>Total URLs Tested:</strong> {len(results.get("url_tests", []))}</p>
        <p><strong>Successful URLs:</strong> {sum(1 for test in results.get("url_tests", []) if test.get("success", False))}</p>
        <p><strong>Failed URLs:</strong> {sum(1 for test in results.get("url_tests", []) if not test.get("success", False))}</p>
        <p><strong>API Endpoints Tested:</strong> {len(results.get("api_tests", []))}</p>
        <p><strong>Screenshots Captured:</strong> {"Yes" if results.get("screenshots_captured", False) else "No"}</p>
    </div>
    
    <div class="section">
        <h2>URL Accessibility Tests</h2>
        <table>
            <tr><th>URL</th><th>Description</th><th>Status Code</th><th>Result</th></tr>
"""

        for test in results.get("url_tests", []):
            status_class = "success" if test.get("success", False) else "error"
            html_content += f"""
            <tr>
                <td>{test.get("url", "N/A")}</td>
                <td>{test.get("description", "N/A")}</td>
                <td>{test.get("status_code", "N/A")}</td>
                <td class="{status_class}">{"✓ PASS" if test.get("success", False) else "✗ FAIL"}</td>
            </tr>
"""

        html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>API Endpoint Tests</h2>
        <table>
            <tr><th>Endpoint</th><th>Status Code</th><th>Result</th></tr>
"""

        for test in results.get("api_tests", []):
            status_class = "success" if test.get("success", False) else "error"
            html_content += f"""
            <tr>
                <td>{test.get("endpoint", "N/A")}</td>
                <td>{test.get("status_code", "N/A")}</td>
                <td class="{status_class}">{"✓ PASS" if test.get("success", False) else "✗ FAIL"}</td>
            </tr>
"""

        html_content += """
        </table>
    </div>
    
    <div class="section">
        <h2>Screenshots</h2>
"""

        # Add screenshots if they exist
        screenshot_files = list(self.screenshot_dir.glob("*.png"))
        if screenshot_files:
            for screenshot in screenshot_files:
                html_content += f'<img src="{screenshot}" alt="{screenshot.stem}" class="screenshot">'
        else:
            html_content += "<p>No screenshots available</p>"

        html_content += """
    </div>
</body>
</html>
"""

        with open(report_path, "w", encoding="utf-8") as f:
            f.write(html_content)

        self.log(f"✓ Test report generated: {report_path}")

    def run_comprehensive_test(self):
        """Run all tests and generate report"""
        self.log("Starting comprehensive UI testing...")

        # Clear previous log
        if self.log_file.exists():
            self.log_file.unlink()

        results = {}

        # Check if server is running
        if not self.check_server_status():
            self.log("Cannot proceed without running server", "ERROR")
            return False

        # Setup test data
        self.setup_test_data()

        # Test URL accessibility
        results["url_tests"] = self.test_url_accessibility()

        # Test authentication
        results["auth_test"] = self.test_authentication_flow()

        # Test API endpoints
        results["api_tests"] = self.test_api_endpoints()

        # Capture screenshots
        results["screenshots_captured"] = self.capture_screenshots_with_puppeteer()

        # Run Django tests
        results["django_tests_passed"] = self.run_django_tests()

        # Generate report
        self.generate_report(results)

        # Summary
        self.log("=" * 50)
        self.log("COMPREHENSIVE TEST SUMMARY")
        self.log("=" * 50)

        url_success_rate = (
            sum(1 for test in results["url_tests"] if test.get("success", False))
            / len(results["url_tests"])
            * 100
            if results["url_tests"]
            else 0
        )
        api_success_rate = (
            sum(1 for test in results["api_tests"] if test.get("success", False))
            / len(results["api_tests"])
            * 100
            if results["api_tests"]
            else 0
        )

        self.log(f"URL Tests: {url_success_rate:.1f}% success rate")
        self.log(f"API Tests: {api_success_rate:.1f}% success rate")
        self.log(f"Authentication: {'✓ PASS' if results['auth_test'] else '✗ FAIL'}")
        self.log(
            f"Screenshots: {'✓ CAPTURED' if results['screenshots_captured'] else '✗ FAILED'}"
        )
        self.log(
            f"Django Tests: {'✓ PASS' if results['django_tests_passed'] else '✗ FAIL'}"
        )

        overall_success = (
            url_success_rate > 80 and api_success_rate > 80 and results["auth_test"]
        )

        self.log(
            f"Overall Status: {'✓ SUCCESS' if overall_success else '✗ ISSUES DETECTED'}"
        )

        return overall_success


def main():
    """Main function"""
    # Configure Django for script execution
    django.setup()

    print("Car Fleet Management System - Comprehensive UI Testing")
    print("=" * 60)

    tester = ComprehensiveUITester()
    success = tester.run_comprehensive_test()

    print("\n" + "=" * 60)
    if success:
        print("🎉 All tests completed successfully!")
        print("📊 Check ui_test_report.html for detailed results")
        print("📸 Screenshots saved in ui_test_screenshots/ directory")
    else:
        print("⚠️  Some tests failed or detected issues")
        print("📋 Check ui_test_log.txt for detailed logs")
        print("📊 Check ui_test_report.html for full report")

    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
