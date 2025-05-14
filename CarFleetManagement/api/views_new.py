from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from django.conf import settings
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import IsAuthenticated, IsAdminUser
import os
import json

from .openrouter_client import get_client
from .report_generator import generate_report

# Import models and serializers
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer
from maintenance.models import Maintenance
from maintenance.serializers import MaintenanceSerializer
# from accounts.models import Driver
# from accounts.serializers import DriverSerializer


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
            # Clean up the temporary file
            if os.path.exists(screenshot_path):
                os.remove(screenshot_path)
            
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
        
        prompt = request.data.get('prompt', None)
        
        try:
            client = get_client()
            results = []
            
            for screenshot_file in screenshot_files:
                screenshot_path = os.path.join(debug_dir, screenshot_file)
                
                # Analyze the screenshot
                analysis = client.analyze_screenshot(screenshot_path, prompt=prompt)
                
                # Add the filename to the analysis
                analysis['filename'] = screenshot_file
                
                results.append(analysis)
            
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
class VehicleListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating vehicles."""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class VehicleRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a vehicle."""
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer
    permission_classes = [IsAuthenticated]


# Maintenance API Views
class MaintenanceListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating maintenance records."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class MaintenanceRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a maintenance record."""
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]


# Driver API Views
class DriverListCreateAPIView(generics.ListCreateAPIView):
    """API view for listing and creating drivers."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()


class DriverRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view for retrieving, updating, and deleting a driver."""
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAuthenticated]
