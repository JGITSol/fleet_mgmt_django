from typing import ClassVar
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from CarFleetManagement.accounts.permissions import ScopedPermission
from CarFleetManagement.accounts.models import UserRole
from CarFleetManagement.telematics.models import GPSLocation, Trip, FuelLog, DriverScore, Alert, Inspection
from .serializers import (
    GPSLocationSerializer, TripSerializer, FuelLogSerializer,
    DriverScoreSerializer, AlertSerializer, InspectionSerializer
)

class GPSLocationListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = GPSLocation.objects.all()
    serializer_class = GPSLocationSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['vehicle']
    ordering_fields = ['timestamp', 'speed']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(vehicle__drivers__user=user)
        return queryset

class TripListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['vehicle', 'driver']
    ordering_fields = ['start_time', 'distance_km']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(driver__user=user)
        return queryset

class FuelLogListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = FuelLog.objects.all()
    serializer_class = FuelLogSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['vehicle', 'driver']
    ordering_fields = ['date', 'cost']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(driver__user=user)
        return queryset

class DriverScoreListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = DriverScore.objects.all()
    serializer_class = DriverScoreSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['driver']
    ordering_fields = ['safety_score', 'eco_score']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(driver__user=user)
        return queryset

class AlertListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = Alert.objects.all()
    serializer_class = AlertSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['vehicle', 'alert_type', 'is_read']
    ordering_fields = ['created_at']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(vehicle__drivers__user=user)
        return queryset

class InspectionListCreateAPIView(generics.ListCreateAPIView):
    required_scope = 'telematics'
    queryset = Inspection.objects.all()
    serializer_class = InspectionSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, ScopedPermission]
    filterset_fields = ['vehicle', 'driver', 'is_pre_trip', 'result']
    ordering_fields = ['date']

    def get_queryset(self):
        queryset = super().get_queryset()
        user = self.request.user
        if user.is_authenticated and getattr(user.role, 'name', None) == UserRole.DRIVER:
            return queryset.filter(driver__user=user)
        return queryset
