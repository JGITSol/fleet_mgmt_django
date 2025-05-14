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

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (MANAGER, 'Manager'),
        (COORDINATOR, 'Coordinator'),
        (DRIVER, 'Driver'),
        (TESTUSER, 'Test User'),
        (MAINTENANCE_STAFF, 'Maintenance Staff'),
    ]

    name = models.CharField(max_length=32, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    permissions = models.JSONField(default=dict, blank=True)

    def __str__(self):
        return self.get_name_display()

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

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.driver_license_number})"
