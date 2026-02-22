from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


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
        (ADMIN, _('Admin')),
        (MANAGER, _('Manager')),
        (COORDINATOR, _('Coordinator')),
        (DRIVER, _('Driver')),
        (TESTUSER, _('Test User')),
        (MAINTENANCE_STAFF, _('Maintenance Staff')),
    ]

    name = models.CharField(max_length=32, choices=ROLE_CHOICES, verbose_name=_('Role Name'))
    description = models.TextField(blank=True, verbose_name=_('Description'))
    permissions = models.JSONField(default=dict, blank=True, verbose_name=_('Permissions'))

    def __str__(self):
        # Avoid relying on Django's auto-generated get_name_display to satisfy static analysis
        return str(self.name)

class CustomUser(AbstractUser):
    """
    Custom user model with support for role-based access and extra profile fields.
    """
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, related_name='users', verbose_name=_('Role'))
    phone_number = models.CharField(max_length=20, blank=True, verbose_name=_('Phone Number'))
    emergency_contact = models.CharField(max_length=100, blank=True, verbose_name=_('Emergency Contact'))

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
    user = models.OneToOneField(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='driver_profile',
        verbose_name=_('User Account'),
    )
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    driver_license_number = models.CharField(max_length=50, unique=True, verbose_name=_('Driver License Number'))
    assigned_vehicles = models.ManyToManyField('vehicles.Vehicle', related_name='drivers', blank=True, verbose_name=_('Assigned Vehicles'))
    phone_number = models.CharField(max_length=20, blank=True, verbose_name=_('Phone Number'))
    email = models.EmailField(blank=True, verbose_name=_('Email'))
    # Driver status to represent whether the driver is active/available.
    STATUS_ACTIVE = 'active'
    STATUS_INACTIVE = 'inactive'
    STATUS_CHOICES: ClassVar[list[tuple[str, str]]] = [
        (STATUS_ACTIVE, _('Active')),
        (STATUS_INACTIVE, _('Inactive')),
    ]

    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_ACTIVE, verbose_name=_('Status'))

    # Optional expiry date for driver's license — some tests expect this field to exist
    license_expiry_date = models.DateField(null=True, blank=True, verbose_name=_('License Expiry Date'))

    # Optional employment dates — make nullable to avoid NOT NULL constraint failures
    hire_date = models.DateField(null=True, blank=True, verbose_name=_('Hire Date'))
    termination_date = models.DateField(null=True, blank=True, verbose_name=_('Termination Date'))

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.driver_license_number})"
