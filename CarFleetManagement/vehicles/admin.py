from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'year', 'vehicle_type', 'status', 'mileage')
    list_filter = ('vehicle_type', 'status', 'brand', 'year')
    search_fields = ('license_plate', 'vin', 'brand', 'model')
    ordering = ('-created_at',)
    readonly_fields = ('created_at', 'updated_at')
