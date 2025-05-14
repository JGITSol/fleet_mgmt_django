from rest_framework import serializers
from .models import Maintenance

from vehicles.serializers import VehicleSerializer, VehicleNestedSerializer

class MaintenanceSerializer(serializers.ModelSerializer):
    days_until_scheduled = serializers.SerializerMethodField()
    vehicle_details = serializers.SerializerMethodField()
    class Meta:
        model = Maintenance
        fields = '__all__'
        extra_fields = ['days_until_scheduled', 'vehicle_details']

    def get_days_until_scheduled(self, obj):
        return obj.days_until_scheduled()

    def get_vehicle_details(self, obj):
        return VehicleNestedSerializer(obj.vehicle).data if obj.vehicle else None
