from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import EmergencyIncident
from .serializers import EmergencyIncidentSerializer

class EmergencyIncidentViewSet(viewsets.ModelViewSet):
    queryset = EmergencyIncident.objects.all()
    serializer_class = EmergencyIncidentSerializer
    permission_classes = [IsAuthenticated]
