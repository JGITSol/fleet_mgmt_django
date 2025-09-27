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
    result = subprocess.run([
        sys.executable, '-m', 'pytest', '--cov=.', '--cov-report=term-missing', '--maxfail=200', '--disable-warnings', '-v'
    ], cwd=root_dir, capture_output=True, text=True)
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


def analyze_root_cause(trace):
    """Very basic root cause analysis based on traceback and error message."""
    if 'ImportError' in trace:
        return 'ImportError: Missing or incorrect import. Check module and class/function names.'
    if 'AssertionError' in trace:
        return 'AssertionError: Test assertion failed. Check expected vs actual values.'
    if 'PermissionDenied' in trace or '403' in trace:
        return 'PermissionDenied: Likely authentication or permissions misconfiguration.'
    if 'TypeError' in trace:
        return 'TypeError: Likely wrong argument types or method signatures.'
    if 'KeyError' in trace:
        return 'KeyError: Dictionary key missing. Check test data and serializers.'
    if 'DoesNotExist' in trace:
        return 'DoesNotExist: Missing object in DB. Check test setup/fixtures.'
    if 'IntegrityError' in trace:
        return 'IntegrityError: DB constraint failed. Check unique fields and test data.'
    if 'ValueError' in trace:
        return 'ValueError: Wrong value passed or returned.'
    if 'NotAuthenticated' in trace:
        return 'NotAuthenticated: Authentication missing in test setup.'
    if 'TemplateDoesNotExist' in trace:
        return 'TemplateDoesNotExist: Missing template file.'
    return 'Unknown: Review full traceback for details.'


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
