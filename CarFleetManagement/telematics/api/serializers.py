from typing import ClassVar
from rest_framework import serializers
from CarFleetManagement.telematics.models import GPSLocation, Trip, FuelLog, DriverScore, Alert, Inspection

class GPSLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = GPSLocation
        fields: ClassVar[list[str]] = ['id', 'vehicle', 'latitude', 'longitude', 'speed', 'heading', 'timestamp']
        read_only_fields: ClassVar[list[str]] = ['id', 'timestamp']

class TripSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trip
        fields: ClassVar[list[str]] = ['id', 'vehicle', 'driver', 'start_time', 'end_time', 'start_location', 'end_location', 'distance_km']
        read_only_fields: ClassVar[list[str]] = ['id']

class FuelLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = FuelLog
        fields: ClassVar[list[str]] = ['id', 'vehicle', 'driver', 'date', 'liters', 'cost', 'odometer', 'receipt_image']
        read_only_fields: ClassVar[list[str]] = ['id', 'date']

class DriverScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = DriverScore
        fields: ClassVar[list[str]] = ['id', 'driver', 'safety_score', 'eco_score', 'total_harsh_brakes', 'total_speeding_events', 'updated_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'updated_at', 'safety_score', 'eco_score', 'total_harsh_brakes', 'total_speeding_events']

class AlertSerializer(serializers.ModelSerializer):
    class Meta:
        model = Alert
        fields: ClassVar[list[str]] = ['id', 'vehicle', 'alert_type', 'message', 'is_read', 'created_at']
        read_only_fields: ClassVar[list[str]] = ['id', 'alert_type', 'message', 'created_at']

class InspectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Inspection
        fields: ClassVar[list[str]] = ['id', 'vehicle', 'driver', 'date', 'is_pre_trip', 'result', 'notes']
        read_only_fields: ClassVar[list[str]] = ['id', 'date']
