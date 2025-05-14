# Testing Documentation

## Overview

This document provides information about the testing setup for the Car Fleet Management application. The project uses pytest with pytest-django for testing Django applications.

## Test Structure

Tests are organized in the `tests/` directory at the project root. The main test files are:

- `test_accounts.py`: Tests for user accounts and authentication
- `test_vehicles.py`: Tests for vehicle management functionality
- `test_maintenance.py`: Tests for maintenance records and scheduling
- `test_emergency.py`: Tests for emergency incident reporting
- `test_api.py`: Tests for REST API endpoints

## Running Tests

### Basic Test Execution

To run all tests:

```bash
python -m pytest
```

To run a specific test file:

```bash
python -m pytest tests/test_maintenance.py
```

To run a specific test:

```bash
python -m pytest tests/test_maintenance.py::test_maintenance_creation
```

### Verbose Output

For more detailed output:

```bash
python -m pytest -v
```

### Test Coverage

To generate a test coverage report:

```bash
python -m pytest --cov=accounts --cov=vehicles --cov=maintenance --cov=emergency --cov=api --cov-report=html
```

The coverage report will be available at `coverage_reports/html/index.html`.

## Test Configuration

The test configuration is defined in:

- `pytest.ini`: Contains pytest configuration settings

## Demo Data Management Commands

To facilitate demos and testing with valid data, custom management commands are provided in the `api/management/commands/` directory:

- `populate_demo_data`: Populates the database with demo vehicles (and can be extended for other models).
- `clear_demo_data`: Removes all demo vehicles from the database.

### Usage

To populate demo data:

```bash
python manage.py populate_demo_data
```

To clear demo data:

```bash
python manage.py clear_demo_data
```

You can extend these commands or add new ones for other demo/test data as needed. See the code in `CarFleetManagement/api/management/commands/` for details.

- `tests/conftest.py`: Contains pytest fixtures and setup code
- `car_fleet_manager/test_settings.py`: Contains Django settings specific to testing

## Test Database

Tests use an in-memory SQLite database for faster execution. The database is created fresh for each test run and destroyed afterward.

## Test Fixtures

Common test fixtures are defined in `tests/conftest.py`:

- `user`: Creates a basic user for testing
- `custom_user`: Creates a user with a role
- `driver`: Creates a driver associated with a user
- `vehicle`: Creates a test vehicle
- `maintenance`: Creates a completed maintenance record
- `scheduled_maintenance`: Creates a scheduled maintenance record
- `emergency_contact`: Creates an emergency contact
- `emergency_incident`: Creates an emergency incident report

## Writing New Tests

When writing new tests:

1. Use the `@pytest.mark.django_db` decorator for tests that need database access
2. Use existing fixtures where possible
3. Follow the naming convention `test_*` for test functions
4. Group related tests in the same test file
5. Keep tests focused on a single functionality
6. Use descriptive test names that explain what is being tested

## Continuous Integration

Tests are automatically run as part of the CI/CD pipeline on GitHub Actions when:

- A pull request is opened
- Code is merged to the main branch
- A new release is created
