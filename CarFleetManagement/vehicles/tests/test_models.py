from django.test import TestCase
from django.utils import timezone
from datetime import timedelta

from vehicles.models import Vehicle

class VehicleTestCase(TestCase):
    """Test cases for the Vehicle model."""
    
    def setUp(self):
        """Set up test environment."""
        self.today = timezone.now().date()
        self.next_service = self.today + timedelta(days=90)
        self.insurance_expiry = self.today + timedelta(days=365)
        
        self.vehicle = Vehicle.objects.create(
            brand='Toyota',
            model='Camry',
            year=2022,
            license_plate='ABC-123',
            vin='1HGCM82633A123456',
            color='Blue',
            fuel_type=Vehicle.FuelType.HYBRID,
            transmission=Vehicle.TransmissionType.AUTOMATIC,
            vehicle_type=Vehicle.VehicleType.SUV,
            mileage=15000,
            last_service_date=self.today - timedelta(days=90),
            next_service_date=self.next_service,
            insurance_expiry=self.insurance_expiry,
            status=Vehicle.Status.AVAILABLE
        )
    
    def test_vehicle_creation(self):
        """Test Vehicle creation."""
        self.assertEqual(self.vehicle.brand, 'Toyota')
        self.assertEqual(self.vehicle.model, 'Camry')
        self.assertEqual(self.vehicle.year, 2022)
        self.assertEqual(self.vehicle.license_plate, 'ABC-123')
        self.assertEqual(self.vehicle.vin, '1HGCM82633A123456')
        self.assertEqual(self.vehicle.color, 'Blue')
        self.assertEqual(self.vehicle.fuel_type, Vehicle.FuelType.HYBRID)
        self.assertEqual(self.vehicle.transmission, Vehicle.TransmissionType.AUTOMATIC)
        self.assertEqual(self.vehicle.vehicle_type, Vehicle.VehicleType.SUV)
        self.assertEqual(self.vehicle.mileage, 15000)
        self.assertEqual(self.vehicle.next_service_date, self.next_service)
        self.assertEqual(self.vehicle.insurance_expiry, self.insurance_expiry)
        self.assertEqual(self.vehicle.status, Vehicle.Status.AVAILABLE)
    
    def test_vehicle_string_representation(self):
        """Test Vehicle string representation."""
        expected_str = 'Toyota Camry (ABC-123)'
        self.assertEqual(str(self.vehicle), expected_str)
    
    def test_vehicle_status_choices(self):
        """Test Vehicle status choices."""
        # Test changing status
        self.vehicle.status = Vehicle.Status.IN_USE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, Vehicle.Status.IN_USE)
        
        self.vehicle.status = Vehicle.Status.MAINTENANCE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, Vehicle.Status.MAINTENANCE)
        
        self.vehicle.status = Vehicle.Status.OUT_OF_SERVICE
        self.vehicle.save()
        self.assertEqual(self.vehicle.status, Vehicle.Status.OUT_OF_SERVICE)
    
    def test_vehicle_fuel_type_choices(self):
        """Test Vehicle fuel type choices."""
        # Test changing fuel type
        self.vehicle.fuel_type = Vehicle.FuelType.DIESEL
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, Vehicle.FuelType.DIESEL)
        
        self.vehicle.fuel_type = Vehicle.FuelType.PETROL
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, Vehicle.FuelType.PETROL)
        
        self.vehicle.fuel_type = Vehicle.FuelType.ELECTRIC
        self.vehicle.save()
        self.assertEqual(self.vehicle.fuel_type, Vehicle.FuelType.ELECTRIC)
    
    def test_vehicle_transmission_choices(self):
        """Test Vehicle transmission choices."""
        # Test changing transmission
        self.vehicle.transmission = Vehicle.TransmissionType.MANUAL
        self.vehicle.save()
        self.assertEqual(self.vehicle.transmission, Vehicle.TransmissionType.MANUAL)
    
    def test_vehicle_type_choices(self):
        """Test Vehicle type choices."""
        # Test changing vehicle type
        self.vehicle.vehicle_type = Vehicle.VehicleType.TRUCK
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, Vehicle.VehicleType.TRUCK)
        
        self.vehicle.vehicle_type = Vehicle.VehicleType.VAN
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, Vehicle.VehicleType.VAN)
        
        self.vehicle.vehicle_type = Vehicle.VehicleType.PICKUP
        self.vehicle.save()
        self.assertEqual(self.vehicle.vehicle_type, Vehicle.VehicleType.PICKUP)