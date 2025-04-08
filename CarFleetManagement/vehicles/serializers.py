from rest_framework import serializers
from .models import Vehicle
from accounts.models import Driver

class DriverNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'full_name']

class VehicleSerializer(serializers.ModelSerializer):
    assigned_drivers = DriverNestedSerializer(many=True, read_only=True)
    maintenance_records = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'vin', 'brand', 'model', 'year', 'vehicle_type',
            'license_plate', 'mileage', 'status', 'fuel_type',
            'transmission', 'color', 'last_service_date',
            'next_service_date', 'insurance_expiry', 'created_at',
            'updated_at', 'assigned_drivers', 'maintenance_records'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']