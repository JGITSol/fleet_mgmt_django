from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models


class UserRole(models.Model):
    """
    Represents a user role in the system, such as Admin, Manager, Coordinator, Driver, or TestUser.
    """
    ADMIN = 'admin'
    MANAGER = 'manager'
    COORDINATOR = 'coordinator'
    DRIVER = 'driver'
    TESTUSER = 'testuser'
    MAINTENANCE_STAFF = 'maintenance_staff'

    ROLE_CHOICES: ClassVar[list[tuple[str, str]]] = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (COORDINATOR, 'Coordinator'),
        (DRIVER, 'Driver'),
        (TESTUSER, 'Test User'),
        (MAINTENANCE_STAFF, 'Maintenance Staff'),
    ]

    name = models.CharField(max_length=32, choices=ROLE_CHOICES)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, blank=True)

    def __str__(self):
        # Avoid relying on Django's auto-generated get_name_display to satisfy static analysis
        return str(self.name)

class CustomUser(AbstractUser):
    """
    Custom user model with support for role-based access and extra profile fields.
    """
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, related_name='users')
    phone_number = models.CharField(max_length=20, blank=True)
    emergency_contact = models.CharField(max_length=100, blank=True)

    @property
    def is_admin(self):
        return self.role and self.role.name == UserRole.ADMIN

    @property
    def is_manager(self):
        return self.role and self.role.name == UserRole.MANAGER

    @property
    def is_coordinator(self):
        return self.role and self.role.name == UserRole.COORDINATOR

    @property
    def is_driver(self):
        return self.role and self.role.name == UserRole.DRIVER

    @property
    def is_testuser(self):
        return self.role and self.role.name == UserRole.TESTUSER


class Driver(models.Model):
    """
    Represents a driver in the fleet management system.
    """
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    driver_license_number = models.CharField(max_length=50, unique=True)
    assigned_vehicles = models.ManyToManyField('vehicles.Vehicle', related_name='drivers', blank=True)
    phone_number = models.CharField(max_length=20, blank=True)
    email = models.EmailField(blank=True)
    # Driver status to represent whether the driver is active/available.
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        (STATUS_ACTIVE, 'Active'),
        (STATUS_INACTIVE, 'Inactive'),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE)

    # Optional expiry date for driver's license — some tests expect this field to exist
    license_expiry_date = models.DateField(null=True, blank=True)

    # Optional employment dates — make nullable to avoid NOT NULL constraint failures
    hire_date = models.DateField(null=True, blank=True, verbose_name='Hire Date')
    termination_date = models.DateField(null=True, blank=True, verbose_name='Termination Date')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.driver_license_number})"
