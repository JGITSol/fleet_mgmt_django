# Fleet Management — System Specification

This document summarizes the core data models, database tables, and API endpoints for the Fleet Management project. It is intended to support code review, API design, and planning work to expand the codebase to industry standards (auditability, constraints, performance, and security).

## Contents
- Models and tables
- API endpoints (paths, methods, permissions)
- Suggested production hardening and extensions
- Linter / CI recommendations

---

## Models

### Vehicle
- Table: `vehicles_vehicle`
- Fields:
  - `id`: AutoField (PK)
  - `brand`: CharField(100), default='Unknown'
  - `model`: CharField(100), default='Unknown'
  - `year`: IntegerField, default=2000
  - `license_plate`: CharField(20), unique=True
  - `vin`: CharField(17), unique=True, default='Unknown'
  - `color`: CharField(50), default='White'
  - `fuel_type`: Choice (DIESEL, PETROL, HYBRID, ELECTRIC)
  - `transmission`: Choice (MANUAL, AUTOMATIC)
  - `vehicle_type`: Choice (TRUCK, VAN, SUV, PICKUP)
  - `mileage`: IntegerField, default=0
  - `last_service_date`: DateField, null=True
  - `next_service_date`: DateField, null=True
  - `insurance_expiry`: DateField, null=True
  - `status`: Choice (AVAILABLE, IN_USE, MAINTENANCE, OUT_OF_SERVICE)
  - `created_at`: DateTimeField
  - `updated_at`: DateTimeField

### Maintenance
- Table: `maintenance_maintenance`
- Fields:
  - `id`: AutoField (PK)
  - `vehicle`: ForeignKey -> Vehicle (CASCADE)
  - `maintenance_type`: Choice (ROUTINE, REPAIR, INSPECTION, OTHER)
  - `status`: Choice (SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED)
  - `description`: TextField
  - `scheduled_date`: DateField
  - `completed_date`: DateField, null=True
  - `odometer_reading`: PositiveIntegerField
  - `cost`: DecimalField(10, 2)
  - `service_provider`: CharField(100)
  - `notes`: TextField, blank=True

### EmergencyIncident
- Table: `emergency_emergencyincident`
- Fields:
  - `id`: AutoField (PK)
  - `vehicle`: ForeignKey -> Vehicle (CASCADE)
  - `driver`: ForeignKey -> Driver (SET_NULL, null=True)
  - `reported_by`: ForeignKey -> CustomUser (CASCADE)
  - `emergency_type`: Choice (ACCIDENT, BREAKDOWN, MEDICAL, THEFT, OTHER)
  - `status`: Choice (REPORTED, RESPONDING, RESOLVED, CLOSED)
  - `location`: CharField(255)
  - `latitude`: DecimalField(9, 6), null=True
  - `longitude`: DecimalField(9, 6), null=True
  - `description`: TextField
  - `reported_time`: DateTimeField (auto)
  - `resolved_time`: DateTimeField, null=True

### EmergencyResponse
- Table: `emergency_emergencyresponse`
- Fields:
  - `id`: AutoField (PK)
  - `incident`: ForeignKey -> EmergencyIncident (CASCADE)
  - `responder`: ForeignKey -> CustomUser (SET_NULL, null=True)
  - `response_time`: DateTimeField (auto)
  - `action_taken`: TextField, null=True
  - `notes`: TextField, blank=True

### Driver
- Table: `accounts_driver`
- Fields:
  - `id`: AutoField (PK)
  - `first_name`: CharField(50)
  - `last_name`: CharField(50)
  - `driver_license_number`: CharField(50), unique=True
  - `assigned_vehicles`: ManyToMany -> Vehicle (via related_name 'drivers')
  - `phone_number`: CharField(20)
  - `email`: EmailField
  - `status`: Choice (active, inactive)
  - `license_expiry_date`: DateField, null=True

---

## API Endpoints

### Authentication (`/api/auth/`)
- `POST register/`: Register new user.
- `POST login/`: JWT Login (returns `user` object + `access` + `refresh`).
- `POST logout/`: Logout (informational for JWT).
- `GET profile/`: Current user profile.
- `GET validate-token/`: Shared JWT validation.

### Core Resources (`/api/`)
| Resource | GET (List) | POST (Create) | GET (Detail) | PUT/PATCH | DELETE |
|----------|------------|---------------|--------------|------------|---------|
| `/vehicles/` | Admin | Admin | Admin | Admin | Admin |
| `/maintenance/` | Admin/Maint | Admin/Maint | Admin/Maint | Admin/Maint | Admin/Maint |
| `/drivers/` | Auth | Auth | Auth | Auth | Auth |
| `/emergencies/` | Auth | Auth | Auth | Auth | Auth |
| `/emergencies/responses/` | Auth | Auth | Auth | Auth | Auth |

### Analytics
- `POST /api/screenshots/analyze/`: Single screenshot analysis.
- `POST /api/screenshots/batch-analyze/`: Automated debug directory sweep.
- `POST /api/screenshots/generate-report/`: HTML report generation from analysis.

---

## Permissions Logic
- **`IsAdminRole`**: Restricts access to Admin users or Django Superusers.
- **`IsAdminOrMaintenanceStaff`**: Allows access for Admin or Maintenance Staff roles.
- **`IsAuthenticated`**: Standard login requirement.

---

## Connectivity & Setup (Flutter Client)

To connect the Flutter application (running on a physical device) to the Django server over a Local Network (WiFi) or VPN:

### 1. Local Network (Same WiFi)
- **Current Test IP**: `192.168.1.12`
- **Start Server Command**: 
  ```powershell
  python manage.py runserver 0.0.0.0:8000
  ```
- **App Configuration (Dart)**: Update the URL in your Flutter code:
  ```dart
  final String baseUrl = 'http://192.168.1.12:8000/api';
  ```
- **Django Auto-Config**: The `CarFleetManagement/settings/dev.py` file is currently configured to dynamically detect and allow `192.168.1.12`.

### 2. Remote / VPN (Tailscale, Cloudflare, etc.)
- **Tailscale/VPN IP**: Identify your Managed IP (e.g., `100.x.y.z`).
- **Production Settings**: Use `prod.py` settings module.
- **App Configuration**: Update `baseUrl` in Flutter to the VPN IP.

### Summary of Current Connection Data
| Requirement | Current Value |
|-------------|---------------|
| **Base URL** | `http://192.168.1.12:8000/api` |
| **PC IP (WiFi)** | `192.168.1.12` |
| **Port** | `8000` |
| **Dev Settings** | `CarFleetManagement.settings.dev` |

Document updated February 2026.
