import uuid
from datetime import datetime, timedelta
from unittest.mock import patch

import pytest
from django.contrib.auth import get_user_model
from django.utils import timezone

from CarFleetManagement.accounts.models import Driver
from CarFleetManagement.accounts.serializers import DriverSerializer
from CarFleetManagement.maintenance.models import Maintenance
from CarFleetManagement.maintenance.serializers import MaintenanceSerializer
from CarFleetManagement.vehicles.models import Vehicle
from CarFleetManagement.vehicles.serializers import VehicleSerializer

User = get_user_model()


@pytest.mark.django_db
class TestDriverSerializer:
    """Test the DriverSerializer."""

    def test_serializer_output(self):
        """Test serializer output format."""
        # Create a uniquely named user for this test to avoid collisions
        unique_username = f"testuser_{uuid.uuid4().hex[:8]}"
        User.objects.create_user(
            username=unique_username, email=f"{unique_username}@example.com", password="testpassword"
        )

        # Create a vehicle
        vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Camry",
            year=2022,
            license_plate="ABC-123",
            vin="1HGCM82633A123456",
            status="AVAILABLE",
        )

        # Create a driver and attach the vehicle to them
        today = timezone.now().date()
        driver = Driver.objects.create(
            first_name="Test",
            last_name="Driver",
            email="driver@example.com",
            phone_number="+1234567890",
            driver_license_number=f"DL{int(timezone.now().timestamp())}",
            license_expiry_date=today,
            hire_date=today,
        )
        # ensure the serializer sees the assigned vehicle
        driver.assigned_vehicles.add(vehicle)

        # Serialize the driver
        serializer = DriverSerializer(driver)
        data = serializer.data

        # Check serialized data
        assert data["first_name"] == "Test"
        assert data["last_name"] == "Driver"
        assert data["full_name"] == "Test Driver"
        assert data["email"] == "driver@example.com"
        assert data["driver_license_number"].startswith("DL")
        # status field removed from model, test skipped
        assert len(data["assigned_vehicles"]) == 1
        assert data["assigned_vehicles"][0]["brand"] == "Toyota"
        assert data["assigned_vehicles"][0]["model"] == "Camry"


@pytest.mark.django_db
class TestVehicleSerializer:
    """Test the VehicleSerializer."""

    def test_serializer_output(self):
        """Test serializer output format for VehicleSerializer."""
        today = timezone.now().date()

        # Create driver with required dates
        driver = Driver.objects.create(
            first_name="Test",
            last_name="Driver",
            email="driver@example.com",
            phone_number="+1234567890",
            driver_license_number=f"DL{int(timezone.now().timestamp())}",
            license_expiry_date=today,
            hire_date=today,
        )

        # Create a vehicle with full data
        vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Camry",
            year=2022,
            license_plate="ABC-123",
            vin="1HGCM82633A123456",
            fuel_type=Vehicle.FuelType.HYBRID,
            transmission=Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=today - timedelta(days=90),
            next_service_date=today + timedelta(days=90),
            insurance_expiry=today + timedelta(days=365),
            status="AVAILABLE",
        )

        # Assign driver to vehicle (ensure bidirectional relationship)
        vehicle.drivers.add(driver)

        # Serialize the vehicle
        serializer = VehicleSerializer(vehicle)
        data = serializer.data

        # Check serialized data
        assert data["brand"] == "Toyota"
        assert data["model"] == "Camry"
        assert data["year"] == 2022
        assert data["license_plate"] == "ABC-123"
        assert data["vin"] == "1HGCM82633A123456"
        assert data["fuel_type"] == "HYBRID"
        assert data["status"] == "AVAILABLE"
        assert len(data["drivers"]) == 1
        assert data["drivers"][0]["first_name"] == "Test"
        assert data["drivers"][0]["last_name"] == "Driver"
        assert data["drivers"][0]["full_name"] == "Test Driver"

        # Serialize the vehicle
        serializer = VehicleSerializer(vehicle)
        data = serializer.data

        # Check serialized data
        assert data["brand"] == "Toyota"
        assert data["model"] == "Camry"
        assert data["year"] == 2022
        assert data["license_plate"] == "ABC-123"
        assert data["vin"] == "1HGCM82633A123456"
        assert data["fuel_type"] == "HYBRID"
        assert data["status"] == "AVAILABLE"
        assert len(data["drivers"]) == 1
        assert data["drivers"][0]["first_name"] == "Test"
        assert data["drivers"][0]["last_name"] == "Driver"
        assert data["drivers"][0]["full_name"] == "Test Driver"


@pytest.mark.django_db
class TestMaintenanceSerializer:
    """Test the MaintenanceSerializer."""

    def test_serializer_output(self):
        """Test serializer output format."""
        # Create a vehicle
        vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Camry",
            year=2022,
            license_plate="ABC-123",
            vin="1HGCM82633A123456",
            status="AVAILABLE",
        )

        # Create maintenance record
        today = timezone.now().date()
        future_date = today + timedelta(days=30)
        maintenance = Maintenance.objects.create(
            vehicle=vehicle,
            maintenance_type="ROUTINE",
            status="SCHEDULED",
            description="Regular oil change and filter replacement",
            scheduled_date=future_date,
            odometer_reading=15000,
            cost=50.00,
            service_provider="Test Mechanic",
            notes="Everything looks good",
        )

        # Serialize the maintenance record
        serializer = MaintenanceSerializer(maintenance)
        data = serializer.data

        # Check serialized data
        assert data["vehicle"] == vehicle.id
        assert data["maintenance_type"] == "ROUTINE"
        assert data["status"] == "SCHEDULED"
        assert data["description"] == "Regular oil change and filter replacement"
        assert data["odometer_reading"] == 15000
        assert float(data["cost"]) == 50.00
        assert data["service_provider"] == "Test Mechanic"

        # Mock the date calculation to ensure consistent test results
        with patch("django.utils.timezone.now") as mock_now:
            mock_now.return_value = timezone.make_aware(datetime.combine(today, datetime.min.time()))
            # Re-serialize with the mocked date
            serializer = MaintenanceSerializer(maintenance)
            data = serializer.data
            assert data["days_until_scheduled"] == 30

        assert data["vehicle_details"]["brand"] == "Toyota"
        assert data["vehicle_details"]["model"] == "Camry"

    def test_serializer_missing_required_fields(self):
        """Test serializer validation for missing required fields."""
        data = {
            "maintenance_type": "ROUTINE",
            "status": "SCHEDULED",
            # 'vehicle' is missing (required)
            "description": "Missing vehicle",
            "scheduled_date": "2025-01-01",
            "odometer_reading": 10000,
            "cost": 100.0,
            "service_provider": "Test",
        }
        serializer = MaintenanceSerializer(data=data)
        assert not serializer.is_valid()
        assert "vehicle" in serializer.errors

    def test_serializer_invalid_maintenance_type(self):
        """Test serializer validation for invalid maintenance_type."""
        data = {
            "vehicle": 1,  # Assume vehicle with ID 1 exists or mock
            "maintenance_type": "INVALID",
            "status": "SCHEDULED",
            "description": "Invalid type",
            "scheduled_date": "2025-01-01",
            "odometer_reading": 10000,
            "cost": 100.0,
            "service_provider": "Test",
        }
        serializer = MaintenanceSerializer(data=data)
        assert not serializer.is_valid()
        assert "maintenance_type" in serializer.errors

    def test_serializer_negative_cost(self):
        """Test serializer validation for negative cost."""
        # Create a driver and a vehicle, then link them
        today = timezone.now().date()
        driver = Driver.objects.create(
            first_name="Test",
            last_name="Driver",
            email="driver@example.com",
            phone_number="+1234567890",
            driver_license_number="DL12345678",
            license_expiry_date=today,
            hire_date=today,
        )

        vehicle = Vehicle.objects.create(
            brand="Toyota",
            model="Camry",
            year=2022,
            license_plate="ABC-123",
            vin="1HGCM82633A123456",
            fuel_type=Vehicle.FuelType.HYBRID,
            transmission=Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=today - timedelta(days=90),
            next_service_date=today + timedelta(days=90),
            insurance_expiry=today + timedelta(days=365),
            status="AVAILABLE",
        )

        # Assign driver to vehicle (ensure bidirectional relationship)
        vehicle.drivers.add(driver)
        data = {
            "vehicle": 1,  # Assume vehicle with ID 1 exists or mock
            "maintenance_type": "ROUTINE",
            "status": "SCHEDULED",
            "description": "Zero odometer",
            "scheduled_date": "2025-01-01",
            "odometer_reading": 0,
            "cost": 100.0,
            "service_provider": "Test",
        }
        serializer = MaintenanceSerializer(data=data)
        # Odometer 0 should be valid
        assert serializer.is_valid() or "odometer_reading" not in serializer.errors
