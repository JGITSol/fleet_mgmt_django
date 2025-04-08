from django.db import models
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.contrib.contenttypes.models import ContentType
from vehicles.models import Vehicle

class DriverStatus(models.TextChoices):
    ACTIVE = 'ACTIVE', _('Active')
    INACTIVE = 'INACTIVE', _('Inactive')
    SUSPENDED = 'SUSPENDED', _('Suspended')

class UserRole(models.Model):
    ADMIN = 'ADMIN'
    FLEET_MANAGER = 'FLEET_MANAGER'
    DRIVER = 'DRIVER'
    MAINTENANCE_STAFF = 'MAINTENANCE_STAFF'
    
    ROLE_CHOICES = [
        (ADMIN, _('Administrator')),
        (FLEET_MANAGER, _('Fleet Manager')),
        (DRIVER, _('Driver')),
        (MAINTENANCE_STAFF, _('Maintenance Staff')),
    ]
    
    name = models.CharField(max_length=100, choices=ROLE_CHOICES, unique=True)
    description = models.TextField(blank=True)
    
    def __str__(self):
        return self.get_name_display()

class CustomUser(AbstractUser):
    role = models.ForeignKey(UserRole, on_delete=models.SET_NULL, null=True, related_name='users')
    phone_number = models.CharField(max_length=20, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role and self.role.name == UserRole.ADMIN
    
    @property
    def is_fleet_manager(self):
        return self.role and self.role.name == UserRole.FLEET_MANAGER
    
    @property
    def is_driver(self):
        return self.role and self.role.name == UserRole.DRIVER
    
    @property
    def is_maintenance_staff(self):
        return self.role and self.role.name == UserRole.MAINTENANCE_STAFF

class Driver(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=50, verbose_name=_('First Name'))
    last_name = models.CharField(max_length=50, verbose_name=_('Last Name'))
    email = models.EmailField(unique=True, verbose_name=_('Email Address'))
    phone_number = models.CharField(max_length=17, blank=True, verbose_name=_('Phone Number'))
    driver_license_number = models.CharField(max_length=20, unique=True, verbose_name=_('Driver License Number'))
    license_expiry_date = models.DateField(verbose_name=_('License Expiry Date'))
    status = models.CharField(max_length=10, choices=DriverStatus.choices, default=DriverStatus.ACTIVE, verbose_name=_('Driver Status'))
    assigned_vehicles = models.ManyToManyField(Vehicle, related_name='assigned_drivers', blank=True, verbose_name=_('Assigned Vehicles'))
    hire_date = models.DateField(verbose_name=_('Hire Date'))
    termination_date = models.DateField(null=True, blank=True, verbose_name=_('Termination Date'))
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

class EmergencyContact(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='emergency_contacts')
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    relationship = models.CharField(max_length=50)
    
    def __str__(self):
        return f"{self.name} ({self.relationship} of {self.user.username})"
