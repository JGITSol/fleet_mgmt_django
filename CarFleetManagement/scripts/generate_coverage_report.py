#!/usr/bin/env python
"""
Generate test coverage report for the CarFleetManagement project.

This script runs the tests with coverage and generates HTML and XML reports.
It can be used to visualize test coverage and identify areas that need more testing.

Usage:
    python scripts/generate_coverage_report.py
"""

import os
import sys
import subprocess
from pathlib import Path

# Add the project root to the path
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

def run_coverage():
    """Run tests with coverage and generate reports."""
    print("\n🔍 Running tests with coverage...")
    
    # Make sure coverage is installed
    try:
        import coverage
    except ImportError:
        print("\n❌ Coverage package not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "coverage"], check=True)
    
    # Create the coverage directory if it doesn't exist
    coverage_dir = project_root / "coverage_reports"
    coverage_dir.mkdir(exist_ok=True)
    
    # Run the tests with coverage
    os.chdir(project_root)
    # First, make sure all test directories are proper Python packages
    for app_dir in project_root.glob('*/'):
        tests_dir = app_dir / 'tests'
        if tests_dir.exists() and tests_dir.is_dir():
            init_file = tests_dir / '__init__.py'
            if not init_file.exists() or os.path.getsize(init_file) == 0:
                print(f"Ensuring {tests_dir} is a proper Python package...")
                with open(init_file, 'w') as f:
                    f.write('# This file makes the tests directory a Python package\n')
    
    result = subprocess.run(
        [
            sys.executable, "manage.py", "test",
            "--settings=test_settings"
        ],
        env={**os.environ, "COVERAGE_PROCESS_START": ".coveragerc"},
        check=False
    )
    
    if result.returncode != 0:
        print(f"\n❌ Tests failed with exit code {result.returncode}")
        return False
    
    # Generate coverage reports
    print("\n📊 Generating coverage reports...")
    
    # Create .coveragerc file if it doesn't exist
    coveragerc_path = project_root / ".coveragerc"
    if not coveragerc_path.exists():
        with open(coveragerc_path, "w") as f:
            f.write("""
[run]
source = .
omit = 
    */migrations/*
    */tests/*
    */test_*
    manage.py
    */settings.py
    */wsgi.py
    */asgi.py
    */apps.py
    */admin.py
    */urls.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise NotImplementedError
    if __name__ == .__main__.:
    pass
    raise ImportError
            """)
    
    # Run coverage
    subprocess.run(
        [sys.executable, "-m", "coverage", "run", "--source=.", "manage.py", "test", "--settings=test_settings"],
        check=True
    )
    
    # Generate HTML report
    html_dir = coverage_dir / "html"
    subprocess.run(
        [sys.executable, "-m", "coverage", "html", "-d", str(html_dir)],
        check=True
    )
    
    # Generate XML report for CI/CD integration
    xml_path = coverage_dir / "coverage.xml"
    subprocess.run(
        [sys.executable, "-m", "coverage", "xml", "-o", str(xml_path)],
        check=True
    )
    
    # Print coverage report to console
    subprocess.run([sys.executable, "-m", "coverage", "report"], check=True)
    
    print(f"\n✅ Coverage reports generated successfully!")
    print(f"\n📁 HTML report: {html_dir}")
    print(f"📄 XML report: {xml_path}")
    
    # Clean up temporary test settings file
    if test_settings_path.exists():
        os.remove(test_settings_path)
        print("Cleaned up temporary test settings file.")
    
    return True

if __name__ == "__main__":
    success = run_coverage()
    sys.exit(0 if success else 1)