
Missing Template Files to Create:
Vehicle Templates:
Create these files in: d:\REPOS\fleet_mgmt_django\CarFleetManagement\vehicles\templates\vehicles\

vehicle_list.html
vehicle_detail.html
vehicle_form.html (used for both create and update views)
Maintenance Templates:
Create these files in: d:\REPOS\fleet_mgmt_django\CarFleetManagement\maintenance\templates\maintenance\

maintenance_list.html
maintenance_detail.html
maintenance_form.html (used for both create and update views)
Template Content:
1. vehicle_list.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}Vehicles{% endblock %}

{% block content %}
<div class="container">
    <h1>Vehicle List</h1>
    <a href="{% url 'vehicle_create' %}" class="btn btn-primary mb-3">Add New Vehicle</a>
    
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Brand</th>
                    <th>Model</th>
                    <th>Year</th>
                    <th>License Plate</th>
                    <th>Status</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for vehicle in vehicles %}
                <tr>
                    <td>{{ vehicle.brand }}</td>
                    <td>{{ vehicle.model }}</td>
                    <td>{{ vehicle.year }}</td>
                    <td>{{ vehicle.license_plate }}</td>
                    <td>{{ vehicle.get_status_display }}</td>
                    <td>
                        <a href="{% url 'vehicle_detail' vehicle.pk %}" class="btn btn-sm btn-info">View</a>
                        <a href="{% url 'vehicle_update' vehicle.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6">No vehicles found.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
2. vehicle_detail.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}{{ vehicle.brand }} {{ vehicle.model }}{% endblock %}

{% block content %}
<div class="container">
    <h1>{{ vehicle.brand }} {{ vehicle.model }}</h1>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ vehicle.year }} {{ vehicle.brand }} {{ vehicle.model }}</h5>
            <p class="card-text"><strong>License Plate:</strong> {{ vehicle.license_plate }}</p>
            <p class="card-text"><strong>VIN:</strong> {{ vehicle.vin }}</p>
            <p class="card-text"><strong>Color:</strong> {{ vehicle.color }}</p>
            <p class="card-text"><strong>Fuel Type:</strong> {{ vehicle.get_fuel_type_display }}</p>
            <p class="card-text"><strong>Transmission:</strong> {{ vehicle.get_transmission_display }}</p>
            <p class="card-text"><strong>Vehicle Type:</strong> {{ vehicle.get_vehicle_type_display }}</p>
            <p class="card-text"><strong>Mileage:</strong> {{ vehicle.mileage }} km</p>
            <p class="card-text"><strong>Status:</strong> {{ vehicle.get_status_display }}</p>
            
            {% if vehicle.last_service_date %}
            <p class="card-text"><strong>Last Service:</strong> {{ vehicle.last_service_date }}</p>
            {% endif %}
            
            {% if vehicle.next_service_date %}
            <p class="card-text"><strong>Next Service:</strong> {{ vehicle.next_service_date }}</p>
            {% endif %}
            
            {% if vehicle.insurance_expiry %}
            <p class="card-text"><strong>Insurance Expiry:</strong> {{ vehicle.insurance_expiry }}</p>
            {% endif %}
            
            <div class="mt-3">
                <a href="{% url 'vehicle_update' vehicle.pk %}" class="btn btn-warning">Edit</a>
                <a href="{% url 'vehicle_list' %}" class="btn btn-secondary">Back to List</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
3. vehicle_form.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}
{% if form.instance.pk %}Edit Vehicle{% else %}Add Vehicle{% endif %}
{% endblock %}

{% block content %}
<div class="container">
    <h1>{% if form.instance.pk %}Edit Vehicle{% else %}Add Vehicle{% endif %}</h1>
    
    <form method="post" novalidate>
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="{{ form.brand.id_for_label }}">Brand</label>
                {{ form.brand }}
                {% if form.brand.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.brand.errors }}
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-6 mb-3">
                <label for="{{ form.model.id_for_label }}">Model</label>
                {{ form.model }}
                {% if form.model.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.model.errors }}
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-4 mb-3">
                <label for="{{ form.year.id_for_label }}">Year</label>
                {{ form.year }}
                {% if form.year.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.year.errors }}
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-4 mb-3">
                <label for="{{ form.license_plate.id_for_label }}">License Plate</label>
                {{ form.license_plate }}
                {% if form.license_plate.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.license_plate.errors }}
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-4 mb-3">
                <label for="{{ form.vin.id_for_label }}">VIN</label>
                {{ form.vin }}
                {% if form.vin.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.vin.errors }}
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Add more form fields as needed -->
        
        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Save</button>
            <a href="{% url 'vehicle_list' %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
4. maintenance_list.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}Maintenance Records{% endblock %}

{% block content %}
<div class="container">
    <h1>Maintenance Records</h1>
    <a href="{% url 'maintenance_create' %}" class="btn btn-primary mb-3">Add New Maintenance Record</a>
    
    <div class="table-responsive">
        <table class="table table-striped">
            <thead>
                <tr>
                    <th>Vehicle</th>
                    <th>Type</th>
                    <th>Status</th>
                    <th>Description</th>
                    <th>Scheduled Date</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                {% for maintenance in maintenance_list %}
                <tr>
                    <td>{{ maintenance.vehicle.brand }} {{ maintenance.vehicle.model }}</td>
                    <td>{{ maintenance.get_maintenance_type_display }}</td>
                    <td>{{ maintenance.get_status_display }}</td>
                    <td>{{ maintenance.description }}</td>
                    <td>{{ maintenance.scheduled_date }}</td>
                    <td>
                        <a href="{% url 'maintenance_detail' maintenance.pk %}" class="btn btn-sm btn-info">View</a>
                        <a href="{% url 'maintenance_update' maintenance.pk %}" class="btn btn-sm btn-warning">Edit</a>
                    </td>
                </tr>
                {% empty %}
                <tr>
                    <td colspan="6">No maintenance records found.</td>
                </tr>
                {% endfor %}
            </tbody>
        </table>
    </div>
</div>
{% endblock %}
5. maintenance_detail.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}Maintenance Details{% endblock %}

{% block content %}
<div class="container">
    <h1>Maintenance Details</h1>
    <div class="card">
        <div class="card-body">
            <h5 class="card-title">{{ maintenance.description }}</h5>
            <p class="card-text"><strong>Vehicle:</strong> {{ maintenance.vehicle.brand }} {{ maintenance.vehicle.model }}</p>
            <p class="card-text"><strong>Type:</strong> {{ maintenance.get_maintenance_type_display }}</p>
            <p class="card-text"><strong>Status:</strong> {{ maintenance.get_status_display }}</p>
            <p class="card-text"><strong>Scheduled Date:</strong> {{ maintenance.scheduled_date }}</p>
            
            {% if maintenance.completed_date %}
            <p class="card-text"><strong>Completed Date:</strong> {{ maintenance.completed_date }}</p>
            {% endif %}
            
            <p class="card-text"><strong>Odometer Reading:</strong> {{ maintenance.odometer_reading }} km</p>
            <p class="card-text"><strong>Cost:</strong> ${{ maintenance.cost }}</p>
            <p class="card-text"><strong>Service Provider:</strong> {{ maintenance.service_provider }}</p>
            
            {% if maintenance.notes %}
            <p class="card-text"><strong>Notes:</strong> {{ maintenance.notes }}</p>
            {% endif %}
            
            <div class="mt-3">
                <a href="{% url 'maintenance_update' maintenance.pk %}" class="btn btn-warning">Edit</a>
                <a href="{% url 'maintenance_list' %}" class="btn btn-secondary">Back to List</a>
            </div>
        </div>
    </div>
</div>
{% endblock %}
6. maintenance_form.html:

html
CopyInsert
{% extends "base.html" %}

{% block title %}
{% if form.instance.pk %}Edit Maintenance Record{% else %}Add Maintenance Record{% endif %}
{% endblock %}

{% block content %}
<div class="container">
    <h1>{% if form.instance.pk %}Edit Maintenance Record{% else %}Add Maintenance Record{% endif %}</h1>
    
    <form method="post" novalidate>
        {% csrf_token %}
        
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="{{ form.vehicle.id_for_label }}">Vehicle</label>
                {{ form.vehicle }}
                {% if form.vehicle.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.vehicle.errors }}
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-6 mb-3">
                <label for="{{ form.maintenance_type.id_for_label }}">Maintenance Type</label>
                {{ form.maintenance_type }}
                {% if form.maintenance_type.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.maintenance_type.errors }}
                </div>
                {% endif %}
            </div>
        </div>
        
        <div class="row">
            <div class="col-md-6 mb-3">
                <label for="{{ form.status.id_for_label }}">Status</label>
                {{ form.status }}
                {% if form.status.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.status.errors }}
                </div>
                {% endif %}
            </div>
            
            <div class="col-md-6 mb-3">
                <label for="{{ form.description.id_for_label }}">Description</label>
                {{ form.description }}
                {% if form.description.errors %}
                <div class="invalid-feedback d-block">
                    {{ form.description.errors }}
                </div>
                {% endif %}
            </div>
        </div>
        
        <!-- Add more form fields as needed -->
        
        <div class="mt-4">
            <button type="submit" class="btn btn-primary">Save</button>
            <a href="{% url 'maintenance_list' %}" class="btn btn-secondary">Cancel</a>
        </div>
    </form>
</div>
{% endblock %}
2. Industry-Standard Solutions for Django Auth Testing
To implement industry-standard solutions for Django auth testing, I recommend the following approach:

Use Django's built-in test client: Instead of the custom patching approach currently used, leverage Django's built-in test client with proper authentication.
Create a test fixture for authentication: Create a base test class that handles authentication for all test cases.
Use factory_boy for test data: Implement factory_boy to create test data consistently.
Here's the code for implementing these solutions:

Create a file d:\REPOS\fleet_mgmt_django\CarFleetManagement\tests\test_utils.py:

python
CopyInsert
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient, APITestCase
from accounts.models import UserRole

User = get_user_model()

class AuthenticatedTestCase(TestCase):
    """Base test case with authentication helpers."""
    
    def setUp(self):
        """Set up test environment with authenticated users."""
        super().setUp()
        
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.FLEET_MANAGER, description='Fleet Manager role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role,
            is_staff=True,
            is_superuser=True
        )
        
        self.fleet_manager_user = User.objects.create_user(
            username='fleet_manager',
            email='fleet@example.com',
            password='password123',
            role=self.fleet_manager_role
        )
        
        self.driver_user = User.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        self.maintenance_user = User.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )
        
        # Create clients
        self.client = Client()
        self.admin_client = Client()
        self.admin_client.login(username='admin_user', password='password123')
        
        self.fleet_manager_client = Client()
        self.fleet_manager_client.login(username='fleet_manager', password='password123')
        
        self.driver_client = Client()
        self.driver_client.login(username='driver_user', password='password123')
        
        self.maintenance_client = Client()
        self.maintenance_client.login(username='maintenance_user', password='password123')


class AuthenticatedAPITestCase(APITestCase):
    """Base test case for API tests with authentication helpers."""
    
    def setUp(self):
        """Set up test environment with authenticated API clients."""
        super().setUp()
        
        # Create roles
        self.admin_role = UserRole.objects.create(name=UserRole.ADMIN, description='Administrator role')
        self.fleet_manager_role = UserRole.objects.create(name=UserRole.FLEET_MANAGER, description='Fleet Manager role')
        self.driver_role = UserRole.objects.create(name=UserRole.DRIVER, description='Driver role')
        self.maintenance_role = UserRole.objects.create(name=UserRole.MAINTENANCE_STAFF, description='Maintenance Staff role')
        
        # Create users
        self.admin_user = User.objects.create_user(
            username='admin_user',
            email='admin@example.com',
            password='password123',
            role=self.admin_role,
            is_staff=True,
            is_superuser=True
        )
        
        self.fleet_manager_user = User.objects.create_user(
            username='fleet_manager',
            email='fleet@example.com',
            password='password123',
            role=self.fleet_manager_role
        )
        
        self.driver_user = User.objects.create_user(
            username='driver_user',
            email='driver@example.com',
            password='password123',
            role=self.driver_role
        )
        
        self.maintenance_user = User.objects.create_user(
            username='maintenance_user',
            email='maintenance@example.com',
            password='password123',
            role=self.maintenance_role
        )
        
        # Create API clients
        self.client = APIClient()  # Unauthenticated client
        
        self.admin_client = APIClient()
        self.admin_client.force_authenticate(user=self.admin_user)
        
        self.fleet_manager_client = APIClient()
        self.fleet_manager_client.force_authenticate(user=self.fleet_manager_user)
        
        self.driver_client = APIClient()
        self.driver_client.force_authenticate(user=self.driver_user)
        
        self.maintenance_client = APIClient()
        self.maintenance_client.force_authenticate(user=self.maintenance_user)
Update d:\REPOS\fleet_mgmt_django\CarFleetManagement\requirements.txt to include factory_boy:

CopyInsert
# Add this to your requirements.txt
factory-boy==3.2.1
3. Fix Date Calculation Issues
To fix date calculation issues in tests, use the freezegun library to freeze time during tests:

Add to requirements.txt:

CopyInsert
freezegun==1.2.2
Example usage in tests:

python
CopyInsert
from freezegun import freeze_time

@freeze_time("2025-04-12")
def test_date_calculation():
    # All date calculations will use 2025-04-12 as the current date
    today = timezone.now().date()
    assert today == date(2025, 4, 12)
Summary of Actions to Take:
Create the missing template files with the content provided above
Create the test utilities file for standardized authentication in tests
Update requirements.txt to include factory_boy and freezegun
Refactor tests to use the new authentication base classes
Use freezegun to fix date calculation issues in tests
These changes will help improve your test coverage and ensure that your tests are more reliable and maintainable.