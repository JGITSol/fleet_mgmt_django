from rest_framework import serializers
from .models import Vehicle
from accounts.models import Driver

class DriverNestedSerializer(serializers.ModelSerializer):
    full_name = serializers.SerializerMethodField()
    class Meta:
        model = Driver
        fields = ['id', 'first_name', 'last_name', 'full_name', 'driver_license_number', 'email', 'phone_number']
    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"

class VehicleSerializer(serializers.ModelSerializer):
    drivers = DriverNestedSerializer(many=True, read_only=True)
    class Meta:
        model = Vehicle
        fields = '__all__'
        extra_fields = ['drivers']

class VehicleNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vehicle
        fields = ['id', 'brand', 'model', 'year', 'license_plate', 'vin', 'status']
