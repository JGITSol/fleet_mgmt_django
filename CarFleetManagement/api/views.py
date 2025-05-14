from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser, BasePermission
from accounts.models import UserRole

class IsAdminOrMaintenanceStaff(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and (
                getattr(request.user, 'role', None) and (
                    request.user.role.name == UserRole.ADMIN or
                    request.user.role.name == UserRole.MAINTENANCE_STAFF
                )
            )
        )

import os
import json

from .openrouter_client import get_client
from .report_generator import generate_report

# Import models and serializers
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from maintenance.models import Maintenance
from maintenance.serializers import MaintenanceSerializer
from accounts.models import Driver
from accounts.serializers import DriverSerializer
from CarFleetManagement.emergency.models import EmergencyIncident
from CarFleetManagement.emergency.models import EmergencyResponse
from CarFleetManagement.emergency.serializers import EmergencyIncidentSerializer, EmergencyResponseSerializer

# Emergency API Views
class EmergencyIncidentListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes = [IsAuthenticated]

class EmergencyIncidentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes = [IsAuthenticated]

class EmergencyIncidentUpdateAPIView(generics.UpdateAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class EmergencyIncidentDeleteAPIView(generics.DestroyAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

class EmergencyResponseCreateView(generics.CreateAPIView):
    queryset = EmergencyResponse.objects.all()
    serializer_class = EmergencyResponseSerializer
    permission_classes = [IsAuthenticated]

from drf_spectacular.utils import extend_schema
from rest_framework.pagination import PageNumberPagination
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics


class AnalyzeScreenshotView(APIView):
    """API view for analyzing a single screenshot using OpenRouter API."""
    
    parser_classes = (MultiPartParser, FormParser)
    
    def post(self, request, format=None):
        # Check if screenshot file is provided
        if 'screenshot' not in request.FILES:
            return Response(
                {"error": "No screenshot file provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        screenshot = request.FILES['screenshot']
        prompt = request.data.get('prompt', None)
        
        # Save the screenshot temporarily
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_screenshots')
        os.makedirs(temp_dir, exist_ok=True)
        
        screenshot_path = os.path.join(temp_dir, screenshot.name)
        with open(screenshot_path, 'wb+') as destination:
            for chunk in screenshot.chunks():
                destination.write(chunk)
        
        try:
            # Analyze the screenshot
            client = get_client()
            analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
            
            # Clean up the temporary file
            os.remove(screenshot_path)
            
            return Response(analysis)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class BatchAnalyzeScreenshotsView(APIView):
    """API view for analyzing multiple screenshots in the debug_screenshots directory."""
    
    def post(self, request, format=None):
        debug_dir = os.path.join(settings.BASE_DIR, 'debug_screenshots')
        
        if not os.path.exists(debug_dir):
            return Response(
                {"error": "Debug screenshots directory does not exist"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Get all PNG files in the directory
        screenshot_files = [f for f in os.listdir(debug_dir) if f.endswith('.png')]

        if not screenshot_files:
            return Response(
                {"error": "No PNG files found in the debug screenshots directory"},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Filtering logic
        language = request.data.get('language')
        theme = request.data.get('theme')
        page = request.data.get('page')
        prompt = request.data.get('prompt', None)

        filtered_files = screenshot_files
        if language:
            filtered_files = [f for f in filtered_files if f"_{language}_" in f]
        if theme:
            filtered_files = [f for f in filtered_files if f"_{theme}_" in f]
        if page:
            filtered_files = [f for f in filtered_files if f.startswith(page)]

        if (language or theme or page) and not filtered_files:
            return Response(
                {"warning": "No screenshots found matching the specified filters."},
                status=status.HTTP_404_NOT_FOUND
            )

        try:
            client = get_client()
            results = {}
            for screenshot_file in filtered_files:
                screenshot_path = os.path.join(debug_dir, screenshot_file)
                # Analyze the screenshot
                analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
                results[screenshot_file] = analysis
            return Response(results)
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


class GenerateReportView(APIView):
    """API view for generating an HTML report from analysis results."""
    
    def post(self, request, format=None):
        analysis_data = request.data.get('analysis_data', None)
        
        if not analysis_data:
            return Response(
                {"error": "No analysis data provided"},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Save analysis data to a temporary file
            temp_dir = os.path.join(settings.BASE_DIR, 'temp_analysis')
            os.makedirs(temp_dir, exist_ok=True)
            
            analysis_file = os.path.join(temp_dir, 'temp_analysis.json')
            with open(analysis_file, 'w') as f:
                json.dump(analysis_data, f)
            
            # Generate the report
            report_path = generate_report(analysis_file)
            
            # Read the report content
            with open(report_path, 'r') as f:
                report_content = f.read()
            
            # Clean up temporary files
            os.remove(analysis_file)
            os.remove(report_path)
            
            # Return the report as HTML
            return HttpResponse(
                report_content,
                content_type='text/html'
            )
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )


# Vehicle API Views
@extend_schema(
    summary="List and create vehicles",
    responses={200: VehicleSerializer(many=True)},
    request=VehicleSerializer,
)
class VehicleListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating vehicles."""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a vehicle."""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


# Maintenance API Views
class MaintenanceListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating maintenance records."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMaintenanceStaff]

    def perform_create(self, serializer):
        serializer.save()


class MaintenanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a maintenance record."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated, IsAdminOrMaintenanceStaff]


# Driver API Views
class DriverListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating drivers."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]

    def perform_create(self, serializer):
        serializer.save()


class DriverRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a driver."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated, IsAdminUser]


class AssignDriverToVehicleAPIView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        driver_id = request.data.get('driver_id')
        driver = Driver.objects.get(id=driver_id)
        vehicle.driver = driver
        vehicle.save()
        return Response({'status': 'driver assigned'})

class UnassignDriverFromVehicleAPIView(generics.UpdateAPIView):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def update(self, request, *args, **kwargs):
        vehicle = self.get_object()
        vehicle.driver = None
        vehicle.save()
        return Response({'status': 'driver unassigned'})
