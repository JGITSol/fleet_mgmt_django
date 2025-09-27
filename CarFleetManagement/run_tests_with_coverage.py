"""
Script to run tests with coverage and save results to a timestamped log file.
"""
import datetime
import subprocess
import sys
from pathlib import Path


def run_tests_with_coverage():
    """Run tests with coverage and save results to a timestamped log file."""
    # Create logs directory if it doesn't exist
    logs_dir = Path("test_logs")
    logs_dir.mkdir(exist_ok=True)

    # Generate timestamp for log file
    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"test_log_{timestamp}.txt"

    # Run tests with coverage and capture output
    print(f"Running tests with coverage. Results will be saved to {log_file}")

    # Command to run tests with coverage
    cmd = [
        sys.executable, "-m", "pytest",
        "--cov=accounts", "--cov=vehicles", "--cov=maintenance",
        "--cov=emergency", "--cov=api", "--cov-report=term", "-v"
    ]

    # Run the command and capture output
    with open(log_file, "w") as f:
        f.write(f"Test run started at: {datetime.datetime.now()}\n")
        f.write(f"Command: {' '.join(cmd)}\n\n")
        f.write("=" * 80 + "\n\n")

        process = subprocess.run(cmd, capture_output=True, text=True)

        f.write("STDOUT:\n")
        f.write(process.stdout)
        f.write("\n\nSTDERR:\n")
        f.write(process.stderr)

        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"Test run completed at: {datetime.datetime.now()}\n")
        f.write(f"Exit code: {process.returncode}\n")

    # Also write to the current timestamp file for quick access
    current_log = logs_dir / "current_test_log.txt"
    with open(current_log, "w") as f:
        f.write(f"Last test run: {datetime.datetime.now()}\n")
        f.write(f"Log file: {log_file}\n\n")

        f.write("STDOUT:\n")
        f.write(process.stdout)
        f.write("\n\nSTDERR:\n")
        f.write(process.stderr)

    print(f"Test results saved to {log_file}")
    print(f"Quick access log: {current_log}")

    # Generate HTML coverage report
    html_dir = Path("coverage_reports/html")
    html_dir.mkdir(parents=True, exist_ok=True)

    subprocess.run([
        sys.executable, "-m", "pytest",
        "--cov=accounts", "--cov=vehicles", "--cov=maintenance",
        "--cov=emergency", "--cov=api", "--cov-report=html:coverage_reports/html"
    ])

    print("HTML coverage report generated at coverage_reports/html/index.html")

    return process.returncode

if __name__ == "__main__":
    sys.exit(run_tests_with_coverage())
