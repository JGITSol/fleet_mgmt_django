# This file can be populated with DRF serializers for the emergency app's models.
from rest_framework import serializers

from CarFleetManagement.accounts.serializers import DriverSerializer

from .models import EmergencyIncident, EmergencyResponse


class EmergencyIncidentSerializer(serializers.ModelSerializer):
    # Represent driver with nested serializer for human-readable name in HTML responses
    driver = DriverSerializer(read_only=True)
    reported_by = serializers.PrimaryKeyRelatedField(read_only=True)
    attachment_url = serializers.SerializerMethodField()

    class Meta:
        model = EmergencyIncident
        fields = [
            'id', 'vehicle', 'driver', 'reported_by', 'emergency_type', 
            'status', 'location', 'latitude', 'longitude', 'description', 
            'reported_time', 'resolved_time', 'attachment', 'video_attachment',
            'attachment_url'
        ]

    def get_attachment_url(self, obj):
        if obj.attachment:
            return obj.attachment.url
        return None

class EmergencyResponseSerializer(serializers.ModelSerializer):
    responder = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EmergencyResponse
        fields = [
            'id', 'incident', 'responder', 'response_time', 
            'action_taken', 'notes', 'attachment'
        ]
