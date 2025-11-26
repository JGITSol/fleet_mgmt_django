#!/usr/bin/env python3
"""
Test API template for errors
"""

import requests


def test_api_template():
    """Test API template"""
    print("🔧 Testing API Template")
    print("=" * 50)

    try:
        response = requests.get("http://localhost:8000/api/", timeout=10)
        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            print("✓ API endpoint accessible")
            print(f"Content length: {len(response.content)} bytes")

            # Check for template errors in response
            content = response.text.lower()
            if (
                "templatesyntaxerror" in content
                or "block" in content
                and "appears more than once" in content
            ):
                print("✗ Template syntax error detected")
                print("Response content (first 500 chars):")
                print(response.text[:500])
                return False
            else:
                print("✓ No template syntax errors detected")
                return True
        else:
            print(f"✗ API endpoint failed: {response.status_code}")
            print("Response content:")
            print(response.text[:500])
            return False

    except Exception as e:
        print(f"✗ Error testing API template: {e}")
        return False


if __name__ == "__main__":
    success = test_api_template()
    if success:
        print("\n✅ API template working correctly!")
    else:
        print("\n❌ API template has issues")
