from rest_framework import serializers

from CarFleetManagement.vehicles.serializers import VehicleSerializer

from .models import Maintenance


class MaintenanceSerializer(serializers.ModelSerializer):
    """
    Serializer for the Maintenance model.
    Provides detailed information about maintenance records, including days until scheduled and vehicle details.
    """

    vehicle_details = VehicleSerializer(source="vehicle", read_only=True)
    days_until_scheduled = serializers.SerializerMethodField()

    class Meta:
        model = Maintenance
        fields = [
            "id",
            "vehicle",
            "vehicle_details",
            "maintenance_type",
            "status",
            "description",
            "scheduled_date",
            "completed_date",
            "odometer_reading",
            "cost",
            "service_provider",
            "notes",
            "days_until_scheduled",
        ]
        read_only_fields = ["id"]
        extra_kwargs = {
            "vehicle": {"help_text": "ID of the vehicle for this maintenance."},
            "maintenance_type": {"help_text": "Type of maintenance (routine, repair, inspection, etc)."},
            "status": {"help_text": "Current status of the maintenance."},
            "description": {"help_text": "Description of the maintenance work."},
            "scheduled_date": {"help_text": "Date the maintenance is scheduled for."},
            "completed_date": {"help_text": "Date the maintenance was completed."},
            "odometer_reading": {"help_text": "Odometer reading at the time of maintenance."},
            "cost": {"help_text": "Cost of the maintenance."},
            "service_provider": {"help_text": "Provider performing the maintenance."},
            "notes": {"help_text": "Additional notes about the maintenance."},
        }

    def get_days_until_scheduled(self, obj):
        return obj.days_until_scheduled()
