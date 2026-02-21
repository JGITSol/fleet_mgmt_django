import json
import os
from typing import ClassVar

from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from drf_spectacular.utils import extend_schema
from rest_framework import generics, status
from rest_framework.parsers import FormParser, JSONParser, MultiPartParser
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.authentication import JWTAuthentication

from CarFleetManagement.accounts.models import Driver, UserRole
from CarFleetManagement.accounts.serializers import DriverSerializer
from CarFleetManagement.emergency.models import EmergencyIncident, EmergencyResponse
from CarFleetManagement.emergency.serializers import (
    EmergencyIncidentSerializer,
    EmergencyResponseSerializer,
)
from CarFleetManagement.maintenance.models import Maintenance
from CarFleetManagement.maintenance.serializers import MaintenanceSerializer
from CarFleetManagement.vehicles.models import Vehicle, VehicleMedia
from CarFleetManagement.vehicles.serializers import VehicleSerializer, VehicleMediaSerializer

from .openrouter_client import get_client
from .report_generator import generate_report


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


class IsAdminRole(BasePermission):
    """Allow access for users with role == ADMIN or is_staff flag set."""
    def has_permission(self, request, view):
        if not (request.user and getattr(request.user, 'is_authenticated', False)):
            return False
        # Allow Django superusers/staffs
        if getattr(request.user, 'is_staff', False) or getattr(request.user, 'is_superuser', False):
            return True
        role = getattr(request.user, 'role', None)
        return bool(role and getattr(role, 'name', None) == UserRole.ADMIN)

    # Emergency API Views
class EmergencyIncidentListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmergencyIncident.objects.all().order_by('-reported_time')
    serializer_class = EmergencyIncidentSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes: ClassVar[list] = [IsAuthenticated]
    pagination_class = None
    ordering = ['-reported_time']

    def create(self, request, *args, **kwargs):
        """Create and, for form POSTs, redirect to the detail HTML page.

        Tests in this project send form-encoded POSTs and expect a 302 redirect
        to the detail page (legacy HTML behavior). For JSON clients we keep
        the normal DRF JSON response.
        """
        is_form = (
            request.content_type.startswith('application/x-www-form-urlencoded')
            or request.content_type.startswith('multipart/form-data')
            or 'text/html' in request.META.get('HTTP_ACCEPT', '')
        )

        print(f"DEBUG: Emergency POST - Content-Type: {request.content_type}")
        # Map 'vehicle_id' to 'vehicle' if provided by the mobile client
        data = request.data.copy()
        if 'vehicle_id' in data and 'vehicle' not in data:
            data['vehicle'] = data['vehicle_id']
            print(f"DEBUG: Remapped vehicle_id {data['vehicle_id']} to vehicle")

        serializer = self.get_serializer(data=data)
        if not serializer.is_valid():
            print(f"DEBUG: Emergency Validation Failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        # Attach the reporting user
        try:
            instance = serializer.save(reported_by=request.user)
            print(f"DEBUG: Emergency Created ID: {instance.id}")
        except Exception as e:
            print(f"DEBUG: Internal Error during save: {str(e)}")
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        headers = self.get_success_headers(serializer.data)

        if is_form:
            # Redirect to a friendly web-detail URL if available.
            try:
                detail_url = f"/emergency/{serializer.data.get('id')}/"
            except Exception:
                detail_url = '/'  # fallback
            return HttpResponseRedirect(detail_url)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmergencyIncidentRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        """Support legacy form-style POST to detail endpoint by treating it as an update.

        If the request looks like a form POST (multipart/form-data or
        application/x-www-form-urlencoded or accepts text/html), perform an
        update and return an HTML redirect to the detail page to match older
        HTML behavior expected by tests.
        """
        is_form = (
            request.content_type.startswith('application/x-www-form-urlencoded')
            or request.content_type.startswith('multipart/form-data')
            or 'text/html' in request.META.get('HTTP_ACCEPT', '')
        )

        response = self.update(request, *args, **kwargs)

        if is_form:
            pk = kwargs.get('pk')
            if not pk:
                try:
                    obj = self.get_object()
                    pk = getattr(obj, 'pk', None)
                except Exception:
                    pk = None

            detail_url = f"/emergency/{pk}/" if pk else '/'
            return HttpResponseRedirect(detail_url)

        return response

class EmergencyIncidentUpdateAPIView(generics.UpdateAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, IsAdminRole]

class EmergencyIncidentDeleteAPIView(generics.DestroyAPIView):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated, IsAdminRole]

class EmergencyResponseListCreateAPIView(generics.ListCreateAPIView):
    queryset = EmergencyResponse.objects.all().order_by('-response_time')
    serializer_class = EmergencyResponseSerializer
    parser_classes = (JSONParser, MultiPartParser, FormParser)
    permission_classes: ClassVar[list] = [IsAuthenticated]
    pagination_class = None
    ordering = ['-response_time']

    def create(self, request, *args, **kwargs):
        is_form = (
            request.content_type.startswith('application/x-www-form-urlencoded')
            or request.content_type.startswith('multipart/form-data')
            or 'text/html' in request.META.get('HTTP_ACCEPT', '')
        )
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # If creating a response via form, attach the current user as responder
        serializer.save(responder=request.user)
        headers = self.get_success_headers(serializer.data)

        if is_form:
            try:
                detail_url = f"/emergency/response/{serializer.data.get('id')}/"
            except Exception:
                detail_url = '/'
            return HttpResponseRedirect(detail_url)

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class EmergencyResponseRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = EmergencyResponse.objects.all()
    serializer_class = EmergencyResponseSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]



class AnalyzeScreenshotView(APIView):
    """API view for analyzing a single screenshot using OpenRouter API."""

    parser_classes = (MultiPartParser, FormParser)

    def post(self, request, format_=None):
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

    def post(self, request, format_=None):
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
                print(f"DEBUG: Analyzing {screenshot_file}")
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

    def post(self, request, format_=None):
        analysis_data = request.data.get('analysis_data', None)
        
        # If not in 'analysis_data' key, try the whole body
        if not analysis_data:
            analysis_data = request.data

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
            with open(report_path) as f:
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
    authentication_classes: ClassVar[list] = [JWTAuthentication]
    queryset = Vehicle.objects.all().order_by('-created_at')
    serializer_class = VehicleSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]
    # Some tests compare response.data directly to serializer.data; disable
    # pagination to keep list responses as plain lists.
    pagination_class = None
    ordering = ['-created_at']

    def perform_create(self, serializer):
        serializer.save()


class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a vehicle."""
    authentication_classes: ClassVar[list] = [JWTAuthentication]
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]


# Maintenance API Views
class MaintenanceListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating maintenance records."""
    queryset = Maintenance.objects.all().order_by('-scheduled_date')
    serializer_class = MaintenanceSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]
    # Some tests compare response.data directly to serializer.data; disable
    # pagination to keep list responses as plain lists.
    pagination_class = None
    ordering = ['-scheduled_date']

    def perform_create(self, serializer):
        serializer.save()


class MaintenanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a maintenance record."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]


# Driver API Views
class DriverListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating drivers."""
    ordering = ['last_name', 'first_name']
    queryset = Driver.objects.all().order_by('last_name', 'first_name')
    serializer_class = DriverSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]
    pagination_class = None

    def perform_create(self, serializer):
        serializer.save()


class DriverRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a driver."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]


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


# Vehicle Media (Gallery) API Views
class VehicleMediaListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating vehicle media (gallery items)."""
    queryset = VehicleMedia.objects.all().order_by('-created_at')
    serializer_class = VehicleMediaSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser, JSONParser)
    pagination_class = None

    def get_queryset(self):
        """Optionally filter by vehicle."""
        queryset = super().get_queryset()
        vehicle_id = self.request.query_params.get('vehicle')
        if vehicle_id:
            queryset = queryset.filter(vehicle_id=vehicle_id)
        return queryset


class VehicleMediaRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a vehicle media item."""
    queryset = VehicleMedia.objects.all()
    serializer_class = VehicleMediaSerializer
    permission_classes: ClassVar[list] = [IsAuthenticated]
