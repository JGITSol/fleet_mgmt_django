from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Maintenance
from .serializers import MaintenanceSerializer

class MaintenanceViewSet(viewsets.ModelViewSet):
    queryset = Maintenance.objects.all()
    serializer_class = MaintenanceSerializer
    permission_classes = [IsAuthenticated]
