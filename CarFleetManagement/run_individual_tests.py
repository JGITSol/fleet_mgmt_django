import os
import subprocess


def run_test_file(file_path):
    """Run a single test file and return the result."""
    print(f"\nRunning tests in {file_path}...")
    result = subprocess.run(
        ["python", "-m", "pytest", file_path, "-v"],
        capture_output=True,
        text=True
    )

    if result.returncode == 0:
        print(f"✅ {file_path} - All tests passed!")
        return True
    else:
        print(f"❌ {file_path} - Tests failed!")
        print(f"Error output: {result.stderr}")
        return False

def main():
    """Run each test file individually."""
    tests_dir = os.path.join(os.getcwd(), "tests")
    test_files = []

    for file in os.listdir(tests_dir):
        if file.startswith("test_") and file.endswith(".py"):
            test_files.append(os.path.join("tests", file))

    print(f"Found {len(test_files)} test files.")

    all_passed = True
    failed_files = []

    for file in test_files:
        if not run_test_file(file):
            all_passed = False
            failed_files.append(file)

    print("\n--- Summary ---")
    if all_passed:
        print("All test files passed successfully!")
    else:
        print(f"{len(failed_files)} test files failed:")
        for file in failed_files:
            print(f"- {file}")

if __name__ == "__main__":
    main()
