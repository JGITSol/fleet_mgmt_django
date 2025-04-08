from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Driver, UserRole, CustomUser, EmergencyContact

@admin.register(Driver)
class DriverAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'driver_license_number', 'status', 'license_expiry_date')
    list_filter = ('status', 'license_expiry_date', 'hire_date')
    search_fields = ('first_name', 'last_name', 'email', 'driver_license_number')
    ordering = ('last_name', 'first_name')
    readonly_fields = ('id',)
    filter_horizontal = ('assigned_vehicles',)

@admin.register(UserRole)
class UserRoleAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'is_staff')
    list_filter = ('role', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('role', 'phone_number', 'profile_picture')}),
    )

@admin.register(EmergencyContact)
class EmergencyContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'relationship', 'phone_number')
    list_filter = ('relationship',)
    search_fields = ('name', 'user__username', 'phone_number')
    raw_id_fields = ('user',)
