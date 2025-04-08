from django.contrib import admin
from .models import Maintenance

@admin.register(Maintenance)
class MaintenanceAdmin(admin.ModelAdmin):
    list_display = ('vehicle', 'maintenance_type', 'status', 'scheduled_date', 'cost')
    list_filter = ('maintenance_type', 'status', 'scheduled_date')
    search_fields = ('vehicle__vin', 'vehicle__license_plate', 'description', 'service_provider')
    ordering = ('-scheduled_date',)
    readonly_fields = ('id',)
    raw_id_fields = ('vehicle',)
