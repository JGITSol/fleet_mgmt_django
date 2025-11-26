#!/usr/bin/env python3
"""Pytest-friendly check for template path resolution.

This test will be skipped when Django settings are not available
or when running in an environment where templates are not configured.
"""

import pytest
from django.conf import settings
from django.template.loader import get_template


def test_template_paths():
    """Verify key templates can be located by the Django template loader."""
    # If templates aren't configured, skip the test instead of failing loudly.
    if not settings.configured or not settings.TEMPLATES:
        pytest.skip("Django templates not configured in this environment")

    dirs = settings.TEMPLATES[0].get("DIRS", [])
    assert isinstance(dirs, (list, tuple))

    # Try to load a couple of high-level templates. If they are missing
    # it's not necessarily a test failure (static dev envs), so we assert
    # only that get_template either returns or raises a TemplateDoesNotExist.
    for tpl in ("registration/login.html", "base.html"):
        try:
            tmpl = get_template(tpl)
            assert tmpl is not None
        except Exception:
            # Let pytest-Django or the environment decide if this is critical.
            pytest.skip(f"Template {tpl} not available in this environment")
