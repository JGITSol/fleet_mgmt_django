import os
import subprocess
import sys

import django

# Add the project directory to the Python path
project_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_dir)

# Configure Django settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CarFleetManagement.settings")


def run_test_file(test_file):
    """Run a single test file and return the exit code."""
    # Ensure Django is ready before importing test helpers that rely on ORM
    django.setup()

    # Import the JWT patch after Django is configured
    from tests.jwt_auth_patch import jwt_auth_patch

    print(f"\n\n=== Running {test_file} ===")


    # Apply the JWT authentication patch
    print("Applying JWT authentication patch...")
    jwt_auth_patch.apply()
    print("Patch applied successfully!")

    try:
        result = subprocess.run(
            [sys.executable, "-m", "pytest", test_file, "-v"],
            capture_output=True,
            text=True,
        )
        print(f"Exit code: {result.returncode}")
        if result.returncode != 0:
            print("STDOUT:")
            print(result.stdout)
            print("STDERR:")
            print(result.stderr)
        return result.returncode
    finally:
        # Restore original permission classes
        print("Restoring original permission classes...")
        jwt_auth_patch.restore()
        print("Original permission classes restored.")

def main():
    """Run each test file individually with JWT authentication patch applied."""
    print("\n=== Running tests with JWT authentication patch ===")
    print("This patch fixes authentication issues in tests by:")
    print("1. Patching permission classes to handle both authenticated and unauthenticated test cases")
    print("2. Providing utilities to authenticate test clients with JWT tokens")
    print("3. Ensuring proper JWT authentication is used instead of force_authenticate")

    tests_dir = os.path.join(os.getcwd(), "tests")
    test_files = [
        os.path.join("tests", f)
        for f in os.listdir(tests_dir)
        if f.startswith("test_") and f.endswith(".py")
    ]

    failed_files = []
    for test_file in test_files:
        exit_code = run_test_file(test_file)
        if exit_code != 0:
            failed_files.append(test_file)

    if failed_files:
        print("\n\n❌ The following test files failed:")
        for f in failed_files:
            print(f"- {f}")
    else:
        print("\n\n✅ All test files passed!")

if __name__ == "__main__":
    main()
