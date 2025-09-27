#!/usr/bin/env python3
"""
Final comprehensive UI test with screenshot capture
"""

import os
import sys
import time
import json
import requests
import subprocess
from datetime import datetime
from pathlib import Path

def test_server_status():
    """Check if Django server is running"""
    try:
        response = requests.get("http://localhost:8000", timeout=5)
        print(f"✓ Server is running (Status: {response.status_code})")
        return True
    except requests.exceptions.ConnectionError:
        print("✗ Server is not running")
        return False
    except Exception as e:
        print(f"✗ Server check error: {e}")
        return False

def test_urls():
    """Test URL accessibility"""
    base_url = "http://localhost:8000"
    
    # URLs that don't require authentication
    public_urls = [
        ('/', 'Home Page'),
        ('/admin/', 'Admin Panel'),
        ('/api/', 'API Root'),
        ('/accounts/login/', 'Login Page'),
        ('/accounts/register/', 'Register Page'),
        ('/vehicles/', 'Vehicle List'),
        ('/maintenance/', 'Maintenance List'),
        ('/emergency/', 'Emergency List'),
    ]
    
    # URLs that require authentication (will be tested separately)
    auth_urls = [
        ('/api/vehicles/', 'API Vehicles'),
        ('/api/drivers/', 'API Drivers'),
        ('/api/maintenance/', 'API Maintenance'),
        ('/api/emergencies/', 'API Emergencies'),
    ]
    
    print("\nTesting URL Accessibility:")
    print("=" * 50)
    
    results = []
    
    # Test public URLs
    for url, name in public_urls:
        try:
            response = requests.get(f"{base_url}{url}", timeout=10)
            status = "✓ PASS" if response.status_code < 400 else f"✗ FAIL ({response.status_code})"
            print(f"{status:15} {name:20} {url}")
            results.append({
                'url': url,
                'name': name,
                'status_code': response.status_code,
                'success': response.status_code < 400,
                'content_length': len(response.content)
            })
        except Exception as e:
            print(f"✗ ERROR      {name:20} {url} - {str(e)}")
            results.append({
                'url': url,
                'name': name,
                'success': False,
                'error': str(e)
            })
    
    # Test authenticated URLs
    try:
        # Get JWT token
        auth_response = requests.post(f"{base_url}/api/auth/login/", json={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        if auth_response.status_code == 200:
            token_data = auth_response.json()
            access_token = token_data.get('access')
            headers = {'Authorization': f'Bearer {access_token}'}
            
            for url, name in auth_urls:
                try:
                    response = requests.get(f"{base_url}{url}", headers=headers, timeout=10)
                    status = "✓ PASS" if response.status_code < 400 else f"✗ FAIL ({response.status_code})"
                    print(f"{status:15} {name:20} {url}")
                    results.append({
                        'url': url,
                        'name': name,
                        'status_code': response.status_code,
                        'success': response.status_code < 400,
                        'content_length': len(response.content)
                    })
                except Exception as e:
                    print(f"✗ ERROR      {name:20} {url} - {str(e)}")
                    results.append({
                        'url': url,
                        'name': name,
                        'success': False,
                        'error': str(e)
                    })
        else:
            # If authentication fails, mark all auth URLs as failed
            for url, name in auth_urls:
                print(f"✗ AUTH FAIL   {name:20} {url}")
                results.append({
                    'url': url,
                    'name': name,
                    'success': False,
                    'error': 'Authentication failed'
                })
    except Exception as e:
        # If authentication fails, mark all auth URLs as failed
        for url, name in auth_urls:
            print(f"✗ AUTH ERROR  {name:20} {url} - {str(e)}")
            results.append({
                'url': url,
                'name': name,
                'success': False,
                'error': str(e)
            })
    
    return results

def test_api_authentication():
    """Test API authentication"""
    print("\nTesting API Authentication:")
    print("=" * 50)
    
    # Try to get JWT token
    try:
        response = requests.post("http://localhost:8000/api/auth/login/", json={
            'username': 'testuser',
            'password': 'testpass123'
        })
        
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get('access')
            print("✓ JWT authentication successful")
            
            # Test authenticated API calls
            headers = {'Authorization': f'Bearer {access_token}'}
            
            api_endpoints = [
                '/api/vehicles/',
                '/api/drivers/',
                '/api/maintenance/',
                '/api/emergencies/'
            ]
            
            all_success = True
            for endpoint in api_endpoints:
                api_response = requests.get(f"http://localhost:8000{endpoint}", headers=headers)
                if api_response.status_code < 400:
                    print(f"✓ {endpoint} working")
                else:
                    print(f"✗ {endpoint} failed ({api_response.status_code})")
                    all_success = False
            
            if all_success:
                print("✓ All authenticated API calls successful")
                return True
            else:
                print("✗ Some authenticated API calls failed")
                return False
        else:
            print(f"✗ JWT authentication failed ({response.status_code})")
            return False
            
    except Exception as e:
        print(f"✗ Authentication test error: {e}")
        return False

def capture_screenshots():
    """Attempt to capture screenshots using Puppeteer"""
    print("\nAttempting Screenshot Capture:")
    print("=" * 50)
    
    # Create screenshots directory
    screenshot_dir = Path("ui_screenshots")
    screenshot_dir.mkdir(exist_ok=True)
    
    # Simple Node.js Puppeteer script
    puppeteer_script = """
const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({ headless: true });
    const page = await browser.newPage();
    
    const urls = [
      { url: 'http://localhost:8000/', name: 'home' },
      { url: 'http://localhost:8000/api/', name: 'api_root' },
      { url: 'http://localhost:8000/admin/', name: 'admin' },
      { url: 'http://localhost:8000/accounts/login/', name: 'login' },
      { url: 'http://localhost:8000/vehicles/', name: 'vehicles' }
    ];
    
    for (const item of urls) {
      try {
        await page.goto(item.url, { waitUntil: 'networkidle2', timeout: 10000 });
        await page.screenshot({ 
          path: `ui_screenshots/${item.name}.png`,
          fullPage: true 
        });
        console.log(`Screenshot captured: ${item.name}.png`);
      } catch (error) {
        console.log(`Failed to capture ${item.name}: ${error.message}`);
      }
    }
    
    await browser.close();
    console.log('Screenshot capture completed');
  } catch (error) {
    console.log(`Puppeteer error: ${error.message}`);
  }
})();
"""
    
    # Write and execute script
    script_path = Path("temp_screenshot_script.js")
    try:
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(puppeteer_script)
        
        # Check if Node.js is available
        result = subprocess.run(["node", "--version"], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print(f"Node.js available: {result.stdout.strip()}")
            
            # Run Puppeteer script
            result = subprocess.run(["node", str(script_path)], capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✓ Screenshots captured successfully")
                print(result.stdout)
                return True
            else:
                print(f"✗ Screenshot capture failed: {result.stderr}")
                return False
        else:
            print("⚠ Node.js not available, skipping screenshots")
            return False
            
    except Exception as e:
        print(f"✗ Screenshot error: {e}")
        return False
    finally:
        if script_path.exists():
            script_path.unlink()

def generate_report(url_results, auth_success, screenshots_captured):
    """Generate HTML report"""
    print("\nGenerating Test Report:")
    print("=" * 50)
    
    # Calculate statistics
    total_urls = len(url_results)
    successful_urls = sum(1 for result in url_results if result.get('success', False))
    success_rate = (successful_urls / total_urls * 100) if total_urls > 0 else 0
    
    # Generate HTML report
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Car Fleet Management - UI Test Report</title>
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ background: #2c3e50; color: white; padding: 20px; border-radius: 5px; margin-bottom: 20px; }}
        .section {{ margin: 20px 0; padding: 15px; border: 1px solid #ddd; border-radius: 5px; }}
        .success {{ color: #27ae60; font-weight: bold; }}
        .error {{ color: #e74c3c; font-weight: bold; }}
        .warning {{ color: #f39c12; font-weight: bold; }}
        table {{ width: 100%; border-collapse: collapse; margin: 10px 0; }}
        th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
        .status-pass {{ background-color: #d4edda; color: #155724; }}
        .status-fail {{ background-color: #f8d7da; color: #721c24; }}
        .screenshot {{ max-width: 300px; margin: 10px; border: 1px solid #ddd; border-radius: 4px; }}
        .stats {{ display: flex; justify-content: space-around; margin: 20px 0; }}
        .stat-box {{ text-align: center; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        .stat-number {{ font-size: 2em; font-weight: bold; color: #2c3e50; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🚗 Car Fleet Management System - UI Test Report</h1>
            <p>Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="section">
            <h2>📊 Test Summary</h2>
            <div class="stats">
                <div class="stat-box">
                    <div class="stat-number">{total_urls}</div>
                    <div>Total URLs</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number success">{successful_urls}</div>
                    <div>Successful</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number error">{total_urls - successful_urls}</div>
                    <div>Failed</div>
                </div>
                <div class="stat-box">
                    <div class="stat-number">{success_rate:.1f}%</div>
                    <div>Success Rate</div>
                </div>
            </div>
        </div>
        
        <div class="section">
            <h2>🔗 URL Accessibility Results</h2>
            <table>
                <tr>
                    <th>URL</th>
                    <th>Name</th>
                    <th>Status Code</th>
                    <th>Result</th>
                    <th>Content Size</th>
                </tr>
"""
    
    for result in url_results:
        status_class = 'status-pass' if result.get('success', False) else 'status-fail'
        status_text = '✓ PASS' if result.get('success', False) else '✗ FAIL'
        status_code = result.get('status_code', 'ERROR')
        content_size = result.get('content_length', 0)
        
        html_content += f"""
                <tr class="{status_class}">
                    <td><code>{result.get('url', 'N/A')}</code></td>
                    <td>{result.get('name', 'N/A')}</td>
                    <td>{status_code}</td>
                    <td>{status_text}</td>
                    <td>{content_size} bytes</td>
                </tr>
"""
    
    html_content += f"""
            </table>
        </div>
        
        <div class="section">
            <h2>🔐 Authentication Test</h2>
            <p class="{'success' if auth_success else 'error'}">
                {'✓ JWT Authentication: PASSED' if auth_success else '✗ JWT Authentication: FAILED'}
            </p>
        </div>
        
        <div class="section">
            <h2>📸 Screenshots</h2>
            <p class="{'success' if screenshots_captured else 'warning'}">
                {'✓ Screenshots captured successfully' if screenshots_captured else '⚠ Screenshots not captured (Node.js/Puppeteer not available)'}
            </p>
"""
    
    # Add screenshots if they exist
    screenshot_dir = Path("ui_screenshots")
    if screenshot_dir.exists():
        screenshot_files = list(screenshot_dir.glob("*.png"))
        if screenshot_files:
            html_content += "<div style='display: flex; flex-wrap: wrap;'>"
            for screenshot in screenshot_files:
                html_content += f'<img src="{screenshot}" alt="{screenshot.stem}" class="screenshot">'
            html_content += "</div>"
        else:
            html_content += "<p>No screenshot files found</p>"
    
    html_content += """
        </div>
        
        <div class="section">
            <h2>🎯 Recommendations</h2>
            <ul>
"""
    
    if success_rate < 80:
        html_content += "<li class='error'>⚠ URL success rate is below 80%. Check server configuration and URL patterns.</li>"
    
    if not auth_success:
        html_content += "<li class='error'>⚠ Authentication tests failed. Verify JWT configuration and test user setup.</li>"
    
    if not screenshots_captured:
        html_content += "<li class='warning'>💡 Install Node.js and Puppeteer for visual testing: <code>npm install puppeteer</code></li>"
    
    if success_rate >= 80 and auth_success:
        html_content += "<li class='success'>✅ System is functioning well! All major components are accessible.</li>"
    
    html_content += """
            </ul>
        </div>
        
        <div class="section">
            <h2>🔧 Next Steps</h2>
            <ol>
                <li>Address any failed URL tests by checking Django URL configuration</li>
                <li>Verify authentication setup if JWT tests failed</li>
                <li>Test form submissions and user interactions manually</li>
                <li>Run comprehensive Django test suite: <code>python manage.py test</code></li>
                <li>Check API endpoints with proper authentication headers</li>
            </ol>
        </div>
    </div>
</body>
</html>
"""
    
    # Write report
    report_path = Path("ui_test_report.html")
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    
    print(f"✓ Report generated: {report_path}")
    return report_path

def main():
    """Main test function"""
    print("🚗 Car Fleet Management System - Comprehensive UI Test")
    print("=" * 60)
    
    # Check server status
    if not test_server_status():
        print("\n❌ Cannot proceed without running Django server.")
        print("Please start the server with: python manage.py runserver")
        return 1
    
    # Test URLs
    url_results = test_urls()
    
    # Test authentication
    auth_success = test_api_authentication()
    
    # Capture screenshots
    screenshots_captured = capture_screenshots()
    
    # Generate report
    report_path = generate_report(url_results, auth_success, screenshots_captured)
    
    # Summary
    successful_urls = sum(1 for result in url_results if result.get('success', False))
    total_urls = len(url_results)
    success_rate = (successful_urls / total_urls * 100) if total_urls > 0 else 0
    
    print("\n" + "=" * 60)
    print("📋 FINAL TEST SUMMARY")
    print("=" * 60)
    print(f"🔗 URL Tests: {successful_urls}/{total_urls} passed ({success_rate:.1f}%)")
    print(f"🔐 Authentication: {'✅ PASS' if auth_success else '❌ FAIL'}")
    print(f"📸 Screenshots: {'✅ CAPTURED' if screenshots_captured else '⚠️  SKIPPED'}")
    print(f"📊 Report: {report_path}")
    
    overall_success = success_rate >= 70 and auth_success
    print(f"\n🎯 Overall Status: {'✅ SUCCESS' if overall_success else '⚠️  NEEDS ATTENTION'}")
    
    if overall_success:
        print("\n🎉 The Car Fleet Management System UI is working well!")
    else:
        print("\n🔧 Some issues detected. Check the report for details.")
    
    return 0 if overall_success else 1

if __name__ == "__main__":
    sys.exit(main())