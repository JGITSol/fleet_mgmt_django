"""Compatibility shim for AuthTestMixin used by older import paths.

Re-exports AuthTestMixin from the canonical location so tests importing
``tests.auth_test_mixin`` continue to work during collection and for static
analysis.
"""
from __future__ import annotations

try:
    from CarFleetManagement.tests.auth_test_mixin import AuthTestMixin
except Exception:  # pragma: no cover - tooling fallback
    from typing import Any

    AuthTestMixin = Any

__all__ = ["AuthTestMixin"]
