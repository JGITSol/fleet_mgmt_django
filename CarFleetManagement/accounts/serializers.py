from rest_framework import serializers
from .models import Driver
from vehicles.serializers import VehicleSerializer

class DriverSerializer(serializers.ModelSerializer):
    assigned_vehicles = VehicleSerializer(many=True, read_only=True)
    full_name = serializers.CharField(read_only=True)

    class Meta:
        model = Driver
        fields = [
            'id', 'first_name', 'last_name', 'full_name', 'email',
            'phone_number', 'driver_license_number', 'license_expiry_date',
            'status', 'assigned_vehicles', 'hire_date', 'termination_date'
        ]
        read_only_fields = ['id']