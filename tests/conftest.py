"""Compatibility shim for test fixtures.

Some test modules import fixtures from ``tests.conftest``. The canonical
conftest lives at the repository root. Re-export the common symbols so those
imports resolve during collection and for static analysis.

This file intentionally contains minimal runtime logic: at runtime pytest will
use fixtures defined in the real top-level `conftest.py` where appropriate.
"""
from __future__ import annotations

try:
    # Import the real top-level symbols when available
    from ..conftest import TEST_PASSWORD, test_password  # type: ignore
except Exception:  # pragma: no cover - tooling fallback
    TEST_PASSWORD = "TestPassword123!"

    def test_password():
        return TEST_PASSWORD

__all__ = ["TEST_PASSWORD", "test_password"]
