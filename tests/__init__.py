# Package initializer for tests to make conftest imports resolvable to static analyzers
from __future__ import annotations

# Re-export TEST_PASSWORD defined in the top-level conftest.py when available
try:
    from conftest import TEST_PASSWORD  # type: ignore
except Exception:
    # During static analysis or other tooling the conftest module may not be importable.
    TEST_PASSWORD = "testpassword123"
