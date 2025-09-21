from typing import ClassVar

from rest_framework import serializers

from CarFleetManagement.accounts.models import Driver

from .models import Vehicle


class DriverNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()

    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'full_name']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}" if obj.first_name and obj.last_name else str(obj)


class VehicleSerializer(serializers.ModelSerializer):
    # The Driver model defines `assigned_vehicles` with related_name='drivers',
    # so on the Vehicle instance the reverse relation is `drivers`.
    # Provide both `assigned_drivers` and `drivers` keys for backward compatibility,
    # but source them from the actual related name.
    assigned_drivers = DriverNestedSerializer(source='drivers', many=True, read_only=True)
    # `drivers` can use the default source (same name) — removing redundant `source` fixes DRF assertion
    drivers = DriverNestedSerializer(many=True, read_only=True)
    maintenance_records = serializers.StringRelatedField(many=True, read_only=True)

    class Meta:
        model = Vehicle
        fields = [
            'id', 'vin', 'brand', 'model', 'year', 'vehicle_type',
            'license_plate', 'mileage', 'status', 'fuel_type',
            'transmission', 'color', 'last_service_date',
            'next_service_date', 'insurance_expiry', 'created_at',
            'updated_at', 'assigned_drivers', 'drivers', 'maintenance_records'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']
