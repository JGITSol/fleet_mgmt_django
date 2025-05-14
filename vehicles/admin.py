from django.contrib import admin
from .models import Vehicle

@admin.register(Vehicle)
class VehicleAdmin(admin.ModelAdmin):
    list_display = ('license_plate', 'brand', 'model', 'year', 'status')
    search_fields = ('license_plate', 'vin', 'brand', 'model')
    list_filter = ('status', 'vehicle_type', 'fuel_type')
