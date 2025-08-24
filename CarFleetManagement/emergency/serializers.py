# This file can be populated with DRF serializers for the emergency app's models.
from rest_framework import serializers
from .models import EmergencyIncident, EmergencyResponse
from CarFleetManagement.accounts.serializers import DriverSerializer



class EmergencyIncidentSerializer(serializers.ModelSerializer):
    # Represent driver with nested serializer for human-readable name in HTML responses
    driver = DriverSerializer(read_only=True)
    reported_by = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EmergencyIncident
        fields = '__all__'

class EmergencyResponseSerializer(serializers.ModelSerializer):
    responder = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = EmergencyResponse
        fields = '__all__'
