from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_type', 'status', 'scheduled_date', 'completed_date')
    search_fields = ('vehicle__license_plate', 'description')
    list_filter = ('maintenance_type', 'status')
