import os
import subprocess
import sys

def run_test_file(test_file):
    """Run a single test file and return the exit code."""
    print(f"\n\n=== Running {test_file} ===")
    result = subprocess.run(
        [sys.executable, "-m", "pytest", test_file, "-v"],
        capture_output=True,
        text=True
    )
    print(f"Exit code: {result.returncode}")
    if result.returncode != 0:
        print("STDOUT:")
        print(result.stdout)
        print("STDERR:")
        print(result.stderr)
    return result.returncode

def main():
    """Run each test file individually."""
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
        print("\n\nThe following test files failed:")
        for f in failed_files:
            print(f"- {f}")
    else:
        print("\n\nAll test files passed!")

if __name__ == "__main__":
    main()
