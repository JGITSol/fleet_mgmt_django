# This file can be populated with DRF serializers for the emergency app's models.
from rest_framework import serializers
from .models import EmergencyIncident, EmergencyResponse

class EmergencyIncidentSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyIncident
        fields = '__all__'

class EmergencyResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyResponse
        fields = '__all__'
