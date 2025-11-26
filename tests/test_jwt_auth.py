#!/usr/bin/env python3
"""Test JWT authentication

This test performs live HTTP calls and will be skipped if the server
is not reachable. Network calls include short timeouts to avoid
blocking the test run.
"""

import pytest
import requests
from requests.exceptions import RequestException


def test_jwt_authentication():
    """Test JWT authentication flow against a running dev server."""
    base_url = "http://localhost:8000"

    # Test login
    login_data = {
        "username": "testuser",
        "password": "testpass123",
    }

    # Use a short timeout so CI doesn't hang if the server is down.
    try:
        response = requests.post(
            f"{base_url}/api/auth/login/", json=login_data, timeout=5
        )
    except RequestException as exc:
        pytest.skip(f"Could not reach {base_url}: {exc}")

    assert response.status_code == 200, (
        f"Login failed: {response.status_code} - {response.text[:200]}"
    )

    token_data = response.json()
    access_token = token_data.get("access")
    assert access_token, "No access token in login response"

    headers = {"Authorization": f"Bearer {access_token}"}

    endpoints = [
        "/api/vehicles/",
        "/api/drivers/",
        "/api/maintenance/",
        "/api/emergencies/",
    ]

    for ep in endpoints:
        try:
            r = requests.get(f"{base_url}{ep}", headers=headers, timeout=5)
        except RequestException as exc:
            pytest.fail(f"Request to {ep} failed: {exc}")
        assert r.status_code < 400, f"Endpoint {ep} returned {r.status_code}"
