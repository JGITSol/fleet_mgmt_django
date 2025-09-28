"""
Re-export TEST_PASSWORD to help test modules import it using different import styles.

This file is only to help static analysis tools resolve imports like
`from conftest import TEST_PASSWORD` used throughout the test-suite. At
runtime pytest will provide fixtures from the top-level `conftest.py`.
"""
try:
    from conftest import TEST_PASSWORD  # type: ignore[attr-defined]
except Exception:
    try:
        from ..conftest import TEST_PASSWORD  # type: ignore[attr-defined]
    except Exception:
        # Fallback for static analysis when conftest is not importable
        TEST_PASSWORD = "testpassword123"

# Provide common test symbols as fallbacks so static analyzers don't report
# F821 undefined names across the test-suite. At runtime pytest/django will
# provide the real objects; these are only for type-checking / linting.
try:
    from CarFleetManagement.accounts.models import CustomUser, UserRole  # type: ignore[attr-defined]
except Exception:  # pragma: no cover - lint-time fallback
    from typing import Any

    CustomUser = Any  # type: ignore[assignment]
    class _UserRoleDummy:
        ADMIN = "ADMIN"

    UserRole = _UserRoleDummy  # type: ignore[assignment]

try:
    # some tests reference a lowercase test_password variable
    from conftest import test_password  # type: ignore[attr-defined]
except Exception:
    try:
        from ..conftest import test_password  # type: ignore[attr-defined]
    except Exception:
        test_password = TEST_PASSWORD  # type: ignore[name-defined]
