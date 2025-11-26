"""Run tests with coverage and save results to a timestamped log file.

This script uses list-style subprocess invocations and a small argument
validator to mitigate S603 findings from security linters. For known-safe
static commands we suppress S603 with an inline noqa and a short explanation.
"""
from __future__ import annotations

import datetime
import subprocess
import sys
from pathlib import Path


def _args_safe(args: list[str]) -> bool:
    """Return True if all args contain only a safe set of characters."""
    safe_chars = set("-_./\\")
    return all(all(c.isalnum() or c in safe_chars for c in a) for a in args)


def run_tests_with_coverage() -> int:
    logs_dir = Path("test_logs")
    logs_dir.mkdir(exist_ok=True)

    timestamp = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
    log_file = logs_dir / f"test_log_{timestamp}.txt"

    print(f"Running tests with coverage. Results will be saved to {log_file}")

    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=accounts",
        "--cov=vehicles",
        "--cov=maintenance",
        "--cov=emergency",
        "--cov=api",
        "--cov-report=term",
        "-v",
    ]

    if not _args_safe(cmd):
        print(f"Refusing to run unsafe command: {cmd}")
        return 1

    # Run the command and capture output
    with open(log_file, "w", encoding="utf-8") as f:
        f.write(f"Test run started at: {datetime.datetime.now()}\n")
        f.write(f"Command: {' '.join(cmd)}\n\n")
        f.write("=" * 80 + "\n\n")

        # Safe invocation; inline noqa documents why S603 is suppressed.
        process = subprocess.run(cmd, capture_output=True, text=True)  # noqa: S603

        f.write("STDOUT:\n")
        f.write(process.stdout)
        f.write("\n\nSTDERR:\n")
        f.write(process.stderr)

        f.write("\n\n" + "=" * 80 + "\n")
        f.write(f"Test run completed at: {datetime.datetime.now()}\n")
        f.write(f"Exit code: {process.returncode}\n")

    current_log = logs_dir / "current_test_log.txt"
    with open(current_log, "w", encoding="utf-8") as f:
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

    html_cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--cov=accounts",
        "--cov=vehicles",
        "--cov=maintenance",
        "--cov=emergency",
        "--cov=api",
        "--cov-report=html:coverage_reports/html",
    ]

    if not _args_safe(html_cmd):
        print(f"Refusing to run unsafe HTML-report command: {html_cmd}")
        return 1

    subprocess.run(html_cmd)  # noqa: S603
    print("HTML coverage report generated at coverage_reports/html/index.html")

    return process.returncode


if __name__ == "__main__":
    raise SystemExit(run_tests_with_coverage())
