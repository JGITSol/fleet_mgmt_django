from datetime import timedelta

from django.utils import timezone
from rest_framework.test import APITestCase


class VehicleTestCase(APITestCase):
    """Test cases for the Vehicle model."""

    def setUp(self):
        """Set up test environment."""
        import uuid
        from CarFleetManagement.vehicles.models import Vehicle
        self.Vehicle = Vehicle
        self.today = timezone.now().date()
        self.next_service = self.today + timedelta(days=90)
        self.insurance_expiry = self.today + timedelta(days=365)
        
        self.license_plate = f'ABC-{uuid.uuid4().hex[:6].upper()}'
        self.vin = f'1HGCM82633A{uuid.uuid4().hex[:6].upper()}'

        self.vehicle = self.Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate=self.license_plate,
            vin=self.vin,
            color='Blue',
            fuel_type=self.Vehicle.FuelType.HYBRID,
            transmission=self.Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=self.Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=self.today - timedelta(days=90),
            next_service_date=self.next_service,
            insurance_expiry=self.insurance_expiry,
            status=self.Vehicle.Status.AVAILABLE
        )

    def test_vehicle_creation(self):
        """Test Vehicle creation."""
        self.assertEqual(self.vehicle.brand, 'Toyota')
        self.assertEqual(self.vehicle.model, 'Camry')
        self.assertEqual(self.vehicle.year, 2022)
        self.assertEqual(self.vehicle.license_plate, self.license_plate)
        self.assertEqual(self.vehicle.vin, self.vin)
        self.assertEqual(self.vehicle.color, 'Blue')
        self.assertEqual(self.vehicle.fuel_type, self.Vehicle.FuelType.HYBRID)
        self.assertEqual(self.vehicle.transmission, self.Vehicle.TransmissionType.AUTOMATIC)
        self.assertEqual(self.vehicle.vehicle_type, self.Vehicle.VehicleType.SUV)
        self.assertEqual(self.vehicle.mileage, 15000)
        self.assertEqual(self.vehicle.next_service_date, self.next_service)
        self.assertEqual(self.vehicle.insurance_expiry, self.insurance_expiry)
        self.assertEqual(self.vehicle.status, self.Vehicle.Status.AVAILABLE)

    def test_vehicle_string_representation(self):
        """Test Vehicle string representation."""
        expected_str = f'Toyota Camry ({self.vehicle.license_plate})'
        self.assertEqual(str(self.vehicle), expected_str)

    def test_vehicle_status_choices(self):
        """Test Vehicle status choices."""
        # Test changing status
        self.vehicle.status = self.Vehicle.Status.IN_USE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, self.Vehicle.Status.IN_USE)

        self.vehicle.status = self.Vehicle.Status.MAINTENANCE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, self.Vehicle.Status.MAINTENANCE)

        self.vehicle.status = self.Vehicle.Status.OUT_OF_SERVICE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, self.Vehicle.Status.OUT_OF_SERVICE)

    def test_vehicle_fuel_type_choices(self):
        """Test Vehicle fuel type choices."""
        # Test changing fuel type
        self.vehicle.fuel_type = self.Vehicle.FuelType.DIESEL
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, self.Vehicle.FuelType.DIESEL)

        self.vehicle.fuel_type = self.Vehicle.FuelType.PETROL
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, self.Vehicle.FuelType.PETROL)

        self.vehicle.fuel_type = self.Vehicle.FuelType.ELECTRIC
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, self.Vehicle.FuelType.ELECTRIC)

    def test_vehicle_transmission_choices(self):
        """Test Vehicle transmission choices."""
        # Test changing transmission
        self.vehicle.transmission = self.Vehicle.TransmissionType.MANUAL
        self.vehicle.save()
        self.assertEqual(self.vehicle.transmission, self.Vehicle.TransmissionType.MANUAL)

    def test_vehicle_type_choices(self):
        """Test Vehicle type choices."""
        # Test changing vehicle type
        self.vehicle.vehicle_type = self.Vehicle.VehicleType.TRUCK
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, self.Vehicle.VehicleType.TRUCK)

        self.vehicle.vehicle_type = self.Vehicle.VehicleType.VAN
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, self.Vehicle.VehicleType.VAN)

        self.vehicle.vehicle_type = self.Vehicle.VehicleType.PICKUP
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, self.Vehicle.VehicleType.PICKUP)
