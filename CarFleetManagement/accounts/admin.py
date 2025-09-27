from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, Driver, UserRole


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'role', 'phone_number')
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('role', 'phone_number', 'emergency_contact')}),
    )

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'driver_license_number', 'phone_number', 'email')
    search_fields = ('first_name', 'last_name', 'driver_license_number')
