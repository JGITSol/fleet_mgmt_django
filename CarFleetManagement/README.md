# CarFleetManagement

[![Release](https://img.shields.io/github/v/release/jgitsol/CarFleetManagement)](https://img.shields.io/github/v/release/jgitsol/CarFleetManagement)
[![Build status](https://img.shields.io/github/actions/workflow/status/jgitsol/CarFleetManagement/main.yml?branch=main)](https://github.com/jgitsol/CarFleetManagement/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/jgitsol/CarFleetManagement/branch/main/graph/badge.svg)](https://codecov.io/gh/jgitsol/CarFleetManagement)
[![Commit activity](https://img.shields.io/github/commit-activity/m/jgitsol/CarFleetManagement)](https://img.shields.io/github/commit-activity/m/jgitsol/CarFleetManagement)
[![License](https://img.shields.io/github/license/jgitsol/CarFleetManagement)](https://img.shields.io/github/license/jgitsol/CarFleetManagement)

This is a template repository for Python projects that use uv for their dependency management.

- **Github repository**: <https://github.com/jgitsol/CarFleetManagement/>
- **Documentation** <https://jgitsol.github.io/CarFleetManagement/>

## Getting started with your project

### 1. Create a New Repository

First, create a repository on GitHub with the same name as this project, and then run the following commands:

```bash
git init -b main
git add .
git commit -m "init commit"
git remote add origin git@github.com:jgitsol/CarFleetManagement.git
git push -u origin main
```

### 2. Set Up Your Development Environment

Then, install the environment and the pre-commit hooks with

```bash
make install
```

This will also generate your `uv.lock` file

### 3. Run the pre-commit hooks

Initially, the CI/CD pipeline might be failing due to formatting issues. To resolve those run:

```bash
uv run pre-commit run -a
```

### 4. Commit the changes

Lastly, commit the changes made by the two steps above to your repository.

```bash
git add .
git commit -m 'Fix formatting issues'
git push origin main
```

You are now ready to start development on your project!
The CI/CD pipeline will be triggered when you open a pull request, merge to main, or when you create a new release.

### 5. Authentication (JWT)

This project uses **JWT authentication** exclusively via [djangorestframework-simplejwt](https://django-rest-framework-simplejwt.readthedocs.io/en/latest/). Legacy token auth is removed.

**Endpoints:**
- `POST /api/auth/register/` — Register a new user (returns JWT tokens)
- `POST /api/auth/login/` — Login (returns JWT tokens)
- `POST /api/auth/logout/` — Logout (client-side token removal)
- `GET /api/auth/profile/` — User profile (requires JWT access token)

**How to authenticate:**
- Obtain tokens from `/api/auth/login/` or `/api/auth/register/`
- Include the `access` token in the `Authorization` header:
  
  ```http
  Authorization: Bearer <access_token>
  ```

### 6. API Documentation

API docs are auto-generated with [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/):
- **OpenAPI schema:** [http://localhost:8000/api/schema/](http://localhost:8000/api/schema/)
- **Swagger UI:** [http://localhost:8000/api/docs/](http://localhost:8000/api/docs/)

You can use Swagger UI to explore and test endpoints interactively.

### 7. Running Tests & Coverage

This project uses pytest for testing. To run the tests, use:

```bash
pytest
```

To run tests with coverage and generate a report:

```bash
pytest --cov --cov-report=html
```

The HTML coverage report will be available at `htmlcov/index.html`.

### 8. Developer Documentation (Sphinx)

Some modules use Python docstrings and Sphinx for developer documentation. To build the docs locally:

```bash
cd docs
make html
```

The documentation will be available in `docs/_build/html/index.html`.

### 9. Django Project Structure

The project is organized into the following main apps:

- **accounts**: User management and authentication
- **vehicles**: Vehicle management and tracking
- **maintenance**: Maintenance records and scheduling
- **emergency**: Emergency incident reporting and management
- **api**: REST API endpoints for the application

To finalize the set-up for publishing to PyPI, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/publishing/#set-up-for-pypi).
For activating the automatic documentation with MkDocs, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/mkdocs/#enabling-the-documentation-on-github).
To enable the code coverage reports, see [here](https://fpgmaas.github.io/cookiecutter-uv/features/codecov/).

## Releasing a new version

---

Repository initiated with [fpgmaas/cookiecutter-uv](https://github.com/fpgmaas/cookiecutter-uv).
