import os

from accounts.models import CustomUser, Driver
from accounts.permissions import IsAdmin, IsAdminOrManager, IsCoordinator, IsManager
from accounts.serializers import CustomUserSerializer, DriverSerializer
from django.conf import settings
from emergency.serializers import EmergencyIncidentSerializer
from maintenance.models import Maintenance
from maintenance.serializers import MaintenanceSerializer
from rest_framework import status, viewsets
from rest_framework.permissions import SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from vehicles.models import Vehicle
from vehicles.serializers import VehicleSerializer

from .openrouter_client import get_client


class UserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [IsAdminOrManager]

class VehicleViewSet(viewsets.ModelViewSet):
    queryset = Vehicle.objects.all()
    serializer_class = VehicleSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdmin() or IsManager() or IsCoordinator()]

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdmin() or IsManager() or IsCoordinator()]

from CarFleetManagement.emergency.models import EmergencyIncident


class EmergencyIncidentViewSet(viewsets.ModelViewSet):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer

    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return [IsAuthenticated()]
        return [IsAdmin() or IsManager() or IsCoordinator()]

class DriverViewSet(viewsets.ModelViewSet):
    queryset = Driver.objects.all()
    serializer_class = DriverSerializer
    permission_classes = [IsAdminOrManager]

class AnalyzeScreenshotView(APIView):
    def post(self, request, *args, **kwargs):
        screenshot = request.FILES.get('screenshot')
        prompt = request.data.get('prompt')
        if not screenshot:
            return Response({'error': 'Screenshot file is required.'}, status=status.HTTP_400_BAD_REQUEST)
        temp_dir = os.path.join(settings.BASE_DIR, 'temp_screenshots')
        os.makedirs(temp_dir, exist_ok=True)
        temp_path = os.path.join(temp_dir, screenshot.name)
        with open(temp_path, 'wb+') as f:
            for chunk in screenshot.chunks():
                f.write(chunk)
        client = get_client()
        result = client.analyze_screenshot(temp_path, prompt=prompt)
        if 'error' in result:
            return Response({'error': result['error']}, status=status.HTTP_400_BAD_REQUEST)
        return Response(result)

class BatchAnalyzeScreenshotsView(APIView):
    def post(self, request, *args, **kwargs):
        language = request.data.get('language')
        theme = request.data.get('theme')
        batch_dir = os.path.join(settings.BASE_DIR, 'test_screenshots')
        client = get_client()
        try:
            results = client.batch_analyze_screenshots(batch_dir, language=language, theme=theme)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        return Response(results)

class GenerateReportView(APIView):
    def post(self, request, *args, **kwargs):
        analysis_data = request.data.get('analysis_data')
        if not analysis_data:
            return Response({'error': 'Analysis data is required.'}, status=status.HTTP_400_BAD_REQUEST)
        # Simulate report generation
        report = {'report': f'Report generated for {len(analysis_data)} items.'}
        return Response(report)
