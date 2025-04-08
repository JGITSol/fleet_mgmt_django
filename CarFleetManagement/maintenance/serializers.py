from rest_framework import serializers
from .models import Maintenance
from vehicles.serializers import VehicleSerializer

class MaintenanceSerializer(serializers.ModelSerializer):
    vehicle_details = VehicleSerializer(source='vehicle', read_only=True)
    days_until_scheduled = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = [
            'id', 'vehicle', 'vehicle_details', 'maintenance_type',
            'status', 'description', 'scheduled_date', 'completed_date',
            'odometer_reading', 'cost', 'service_provider', 'notes',
            'days_until_scheduled'
        ]
        read_only_fields = ['id']
    
    def get_days_until_scheduled(self, obj):
        return obj.days_until_scheduled()