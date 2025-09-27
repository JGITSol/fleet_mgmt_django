from typing import Optional

import requests

API_BASE_URL = "http://localhost:8000/api"

class APIClient:
    def __init__(self):
        self.access_token: Optional[str] = None

    def set_token(self, token: str):
        self.access_token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.access_token:
            headers["Authorization"] = f"Bearer {self.access_token}"
        return headers

    def login(self, username: str, password: str):
        resp = requests.post(f"{API_BASE_URL}/accounts/login/", json={"username": username, "password": password})
        resp.raise_for_status()
        data = resp.json()
        self.set_token(data["access"])
        return data

    def logout(self):
        if not self.access_token:
            return
        resp = requests.post(f"{API_BASE_URL}/accounts/logout/", headers=self._headers())
        resp.raise_for_status()
        self.access_token = None
        return resp.json()

    def get_vehicles(self):
        resp = requests.get(f"{API_BASE_URL}/vehicles/", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_vehicle(self, payload):
        resp = requests.post(f"{API_BASE_URL}/vehicles/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def update_vehicle(self, vehicle_id, payload):
        resp = requests.put(f"{API_BASE_URL}/vehicles/{vehicle_id}/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def delete_vehicle(self, vehicle_id):
        resp = requests.delete(f"{API_BASE_URL}/vehicles/{vehicle_id}/", headers=self._headers())
        resp.raise_for_status()
        return resp.status_code == 204

    def get_drivers(self):
        resp = requests.get(f"{API_BASE_URL}/drivers/", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_driver(self, payload):
        resp = requests.post(f"{API_BASE_URL}/drivers/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def update_driver(self, driver_id, payload):
        resp = requests.put(f"{API_BASE_URL}/drivers/{driver_id}/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def delete_driver(self, driver_id):
        resp = requests.delete(f"{API_BASE_URL}/drivers/{driver_id}/", headers=self._headers())
        resp.raise_for_status()
        return resp.status_code == 204

    def get_maintenance(self):
        resp = requests.get(f"{API_BASE_URL}/maintenance/", headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def create_maintenance(self, payload):
        resp = requests.post(f"{API_BASE_URL}/maintenance/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def update_maintenance(self, maintenance_id, payload):
        resp = requests.put(f"{API_BASE_URL}/maintenance/{maintenance_id}/", json=payload, headers=self._headers())
        resp.raise_for_status()
        return resp.json()

    def delete_maintenance(self, maintenance_id):
        resp = requests.delete(f"{API_BASE_URL}/maintenance/{maintenance_id}/", headers=self._headers())
        resp.raise_for_status()
        return resp.status_code == 204

api_client = APIClient()
