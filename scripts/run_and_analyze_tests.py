#!/usr/bin/env python3
"""
run_and_analyze_tests.py

Runs all pytest tests, parses the results, and performs root cause analysis on any failures.
Prints a summary of failures and their likely root causes.
"""
import re
import subprocess
import sys


def run_pytest():
    """Run pytest with coverage, verbose output, and capture the results from the project root."""
    import os
    print("Running all tests with pytest + coverage...\n")
    root_dir = os.path.dirname(os.path.abspath(__file__))
    cmd = [
        sys.executable,
        '-m',
        'pytest',
        '--cov=.',
        '--cov-report=term-missing',
        '--maxfail=200',
        '--disable-warnings',
        '-v',
    ]

    if not all(all(c.isalnum() or c in "-_./\\" for c in a) for a in cmd):
        raise RuntimeError(f"Refusing to run unsafe command: {cmd}")

    result = subprocess.run(
        cmd,
        cwd=root_dir,
        capture_output=True,
        text=True,
        timeout=600,
    )  # noqa: S603
    with open(os.path.join(root_dir, 'last_pytest_output.txt'), 'w', encoding='utf-8') as f:
        f.write(result.stdout)
        f.write(result.stderr)
    return result.stdout + result.stderr


def parse_failures(output):
    """Extract failing test names and error messages from pytest output."""
    failures = []
    lines = output.splitlines()
    current_test = None
    current_trace = []
    in_failure = False
    for line in lines:
        if re.match(r'^_{3,}\s+([\w\d_.:/\\]+)\s+_{3,}$', line):
            # Start of a failure block
            if current_test and current_trace:
                failures.append((current_test, '\n'.join(current_trace)))
            current_test = re.sub(r'^_{3,}\s+|\s+_{3,}$', '', line)
            current_trace = []
            in_failure = True
        elif in_failure:
            # End of failure block
            if line.startswith('=') and 'FAILURES' not in line:
                in_failure = False
                if current_test and current_trace:
                    failures.append((current_test, '\n'.join(current_trace)))
                current_test = None
                current_trace = []
            else:
                current_trace.append(line)
    if current_test and current_trace:
        failures.append((current_test, '\n'.join(current_trace)))
    return failures


def analyze_root_cause(trace: str) -> str:
    """Lightweight root cause hints extracted from traceback text.

    This function intentionally keeps a short list of common error
    signatures to stay under complexity limits enforced by linters.
    """
    keywords = [
        ('ImportError', 'ImportError: missing/incorrect import.'),
        ('AssertionError', 'AssertionError: assertion failed.'),
        ('PermissionDenied', 'PermissionDenied: likely permissions/auth issue.'),
        ('403', 'HTTP 403 response: permission/authentication problem.'),
        ('TypeError', 'TypeError: wrong argument type or signature.'),
        ('KeyError', 'KeyError: missing dict key in test data.'),
        ('DoesNotExist', 'DoesNotExist: DB object missing; check fixtures.'),
        ('IntegrityError', 'IntegrityError: DB constraint violation.'),
        ('ValueError', 'ValueError: invalid value passed.'),
        ('TemplateDoesNotExist', 'TemplateDoesNotExist: missing template file.'),
    ]
    for key, msg in keywords:
        if key in trace:
            return msg
    return 'Unknown: review full traceback for details.'


def parse_test_results(output):
    """Extract all test names and their result (PASSED/FAILED/SKIPPED) from pytest output."""
    test_results = []
    # Example: CarFleetManagement/tests/test_accounts.py::test_custom_user_creation PASSED [  2%]
    test_line = re.compile(r'([\w./\\:-]+)\s+(PASSED|FAILED|SKIPPED|ERROR|XFAIL|XPASS)')
    for line in output.splitlines():
        m = test_line.search(line)
        if m:
            test_results.append((m.group(1), m.group(2)))
    return test_results

def print_results_table(test_results):
    """Print a table of all test results with a summary score and basic coverage info."""
    passed = sum(1 for _, status in test_results if status == 'PASSED')
    failed = sum(1 for _, status in test_results if status in ('FAILED', 'ERROR'))
    skipped = sum(1 for _, status in test_results if status == 'SKIPPED')
    total = len(test_results)
    coverage = 100.0 * passed / total if total else 0.0
    print("\nTest Results Summary:")
    print(f"  Total tests:   {total}")
    print(f"  Passed:        {passed}")
    print(f"  Failed:        {failed}")
    print(f"  Skipped:       {skipped}")
    print(f"  Test run coverage: {coverage:.1f}% (pass rate)\n")
    print(f"{'Status':<8} | Test Name")
    print(f"{'-'*8}-+-{'-'*60}")
    for name, status in test_results:
        print(f"{status:<8} | {name}")
    print()
    print("Note: This is test run coverage (pass rate), not code coverage.")
    print("To measure code coverage, run: pytest --cov . --cov-report=term-missing\n")

def print_coverage_report(output):
    """Extract and print the pytest-cov coverage report from pytest output."""
    print("\nCode Coverage Report:")
    in_report = False
    for line in output.splitlines():
        if '----------' in line and not in_report:
            in_report = True
            print(line)
        elif in_report:
            print(line)
            if line.strip() == '':
                break

def main():
    output = run_pytest()
    test_results = parse_test_results(output)
    print_results_table(test_results)
    print_coverage_report(output)
    failures = parse_failures(output)
    if not failures:
        print("All tests passed!\n")
        return
    print(f"\n{len(failures)} test(s) failed. Root cause analysis:")
    for test, trace in failures:
        print("\n===", test, "===")
        print('\n'.join(trace.split('\n')[-10:]))  # Show last 10 lines of traceback
        print("Root Cause:", analyze_root_cause(trace))

if __name__ == "__main__":
    main()
