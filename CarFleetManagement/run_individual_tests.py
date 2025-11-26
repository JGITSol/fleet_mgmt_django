import os
import subprocess
import sys


def _is_safe_path(path: str) -> bool:
    """Basic safety check: path should be relative, not contain parent-up segments and reside under tests/"""
    if not isinstance(path, str):
        return False
    if ".." in path:
        return False
    # Must be inside tests/ directory
    return path.startswith("tests/")


def run_test_file(file_path):
    """Run a single test file and return the result."""
    print(f"\nRunning tests in {file_path}...")
    # Use current Python executable and validate file path
    if not _is_safe_path(file_path):
        print(f"Unsafe path refused: {file_path}")
        return False

    cmd = [sys.executable, "-m", "pytest", file_path, "-v"]

    # Basic argument sanity check: permit typical path characters and flags
    def _args_safe(args: list[str]) -> bool:
        for a in args:
            # allow alnum, dash, underscore, dot and path separator
            if not all(c.isalnum() or c in "-_./\\" for c in a):
                return False
        return True

    if not _args_safe(cmd):
        print(f"Refusing to run unsafe command: {cmd}")
        return False

    # cmd validated above by _args_safe; suppress S603 for this safe invocation
    result = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603

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
