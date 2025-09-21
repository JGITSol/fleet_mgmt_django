from typing import ClassVar

from rest_framework import serializers

from CarFleetManagement.vehicles.models import Vehicle

from .models import CustomUser, Driver, UserRole


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = ['id', 'name', 'description', 'permissions']

class CustomUserSerializer(serializers.ModelSerializer):
    role = UserRoleSerializer(read_only=True)
    is_admin = serializers.ReadOnlyField()
    is_manager = serializers.ReadOnlyField()
    is_coordinator = serializers.ReadOnlyField()
    is_driver = serializers.ReadOnlyField()
    is_testuser = serializers.ReadOnlyField()

    class Meta:
        model = CustomUser
        fields = [
            'id', 'username', 'email', 'role', 'phone_number', 'emergency_contact',
            'is_admin', 'is_manager', 'is_coordinator', 'is_driver', 'is_testuser'
        ]


class VehicleNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year', 'license_plate', 'vin']

class DriverSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    assigned_vehicles = VehicleNestedSerializer(many=True, read_only=True)
    
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'full_name', 'driver_license_number', 'assigned_vehicles', 'phone_number', 'email']

    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"
