"""Compatibility re-exports for test helpers.

Some test modules import helpers as ``from tests.auth_utils import ...``. The
canonical implementations live under ``CarFleetManagement/tests``. Create a
thin shim that re-exports those symbols so both runtime test collection and
static analysis resolve imports uniformly.

These shims provide conservative fallbacks only for tooling when the real
test helpers are not importable; at runtime pytest will use fixtures and the
real implementations.
"""
from __future__ import annotations

try:  # Prefer the real helpers from the package
    from CarFleetManagement.tests.auth_utils import (
        AuthUtils,
        jwt_auth_patch,
        get_authenticated_client,
        authenticate_client,
    )
    # AuthTestMixin is defined in either auth_test_mixin.py or at the bottom of
    # CarFleetManagement.tests.auth_utils. Try to import it for convenience.
    try:
        from CarFleetManagement.tests.auth_test_mixin import AuthTestMixin  # type: ignore
    except Exception:
        try:
            from CarFleetManagement.tests.auth_utils import AuthTestMixin  # type: ignore
        except Exception:
            AuthTestMixin = None  # pragma: no cover - tooling fallback
except Exception:  # pragma: no cover - tooling fallback
    from typing import Any

    AuthUtils = Any

    def jwt_auth_patch(*args, **kwargs):  # pragma: no cover - tooling fallback
        raise RuntimeError("jwt_auth_patch shim used outside test runtime")

    def get_authenticated_client(*args, **kwargs):  # pragma: no cover
        raise RuntimeError("get_authenticated_client shim used outside test runtime")

    def authenticate_client(*args, **kwargs):  # pragma: no cover
        raise RuntimeError("authenticate_client shim used outside test runtime")

__all__ = [
    "AuthUtils",
    "jwt_auth_patch",
    "get_authenticated_client",
    "authenticate_client",
    "AuthTestMixin",
]
