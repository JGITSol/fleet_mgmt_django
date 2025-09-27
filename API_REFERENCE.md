# Car Fleet Management API Reference

## Overview

The Car Fleet Management API provides comprehensive REST endpoints for managing vehicles, drivers, maintenance records, and emergency incidents. The API uses JWT authentication and follows REST conventions.

**Base URL**: `http://localhost:8000/api/`  
**Authentication**: JWT Bearer Token  
**Content Type**: `application/json`

## Authentication

### JWT Token Authentication

All API endpoints require authentication using JWT tokens. Include the token in the Authorization header:

```
Authorization: Bearer <access_token>
```

### Authentication Endpoints

#### Register User
```http
POST /api/auth/register/
Content-Type: application/json

{
    "username": "string",
    "email": "string",
    "password": "string",
    "first_name": "string",
    "last_name": "string"
}
```

**Response (201 Created)**:
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe"
}
```

#### Login
```http
POST /api/auth/login/
Content-Type: application/json

{
    "username": "string",
    "password": "string"
}
```

**Response (200 OK)**:
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user": {
        "id": 1,
        "username": "john_doe",
        "email": "john@example.com"
    }
}
```

#### Get User Profile
```http
GET /api/auth/profile/
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "role": {
        "name": "driver",
        "description": "Driver role"
    }
}
```

#### Validate Token
```http
POST /api/auth/validate-token/
Content-Type: application/json

{
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

## Vehicle Management

### List Vehicles
```http
GET /api/vehicles/
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `status`: Filter by status (AVAILABLE, IN_USE, MAINTENANCE, OUT_OF_SERVICE)
- `vehicle_type`: Filter by type (TRUCK, VAN, SUV, PICKUP)
- `search`: Search in brand, model, license_plate

**Response (200 OK)**:
```json
{
    "count": 25,
    "next": "http://localhost:8000/api/vehicles/?page=2",
    "previous": null,
    "results": [
        {
            "id": 1,
            "vin": "1HGBH41JXMN109186",
            "brand": "Toyota",
            "model": "Camry",
            "year": 2022,
            "vehicle_type": "SUV",
            "license_plate": "ABC-123",
            "mileage": 15000,
            "status": "AVAILABLE",
            "fuel_type": "PETROL",
            "transmission": "AUTOMATIC",
            "color": "White",
            "last_service_date": "2024-01-15",
            "next_service_date": "2024-07-15",
            "insurance_expiry": "2024-12-31",
            "created_at": "2024-01-01T10:00:00Z",
            "updated_at": "2024-01-15T14:30:00Z",
            "assigned_drivers": [],
            "maintenance_records": []
        }
    ]
}
```

### Create Vehicle
```http
POST /api/vehicles/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "vin": "1HGBH41JXMN109186",
    "brand": "Toyota",
    "model": "Camry",
    "year": 2022,
    "vehicle_type": "SUV",
    "license_plate": "ABC-123",
    "mileage": 15000,
    "fuel_type": "PETROL",
    "transmission": "AUTOMATIC",
    "color": "White",
    "last_service_date": "2024-01-15",
    "next_service_date": "2024-07-15",
    "insurance_expiry": "2024-12-31"
}
```

### Get Vehicle Details
```http
GET /api/vehicles/{id}/
Authorization: Bearer <access_token>
```

### Update Vehicle
```http
PUT /api/vehicles/{id}/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "mileage": 16000,
    "status": "IN_USE"
}
```

### Delete Vehicle
```http
DELETE /api/vehicles/{id}/
Authorization: Bearer <access_token>
```

## Driver Management

### List Drivers
```http
GET /api/drivers/
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
    "count": 15,
    "results": [
        {
            "id": 1,
            "first_name": "John",
            "last_name": "Doe",
            "full_name": "John Doe",
            "email": "john.doe@example.com",
            "phone_number": "+1234567890",
            "driver_license_number": "D123456789",
            "license_expiry_date": "2025-12-31",
            "status": "ACTIVE",
            "hire_date": "2023-01-15",
            "termination_date": null,
            "assigned_vehicles": [
                {
                    "id": 1,
                    "license_plate": "ABC-123",
                    "brand": "Toyota",
                    "model": "Camry"
                }
            ]
        }
    ]
}
```

### Create Driver
```http
POST /api/drivers/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com",
    "phone_number": "+1234567890",
    "driver_license_number": "D123456789",
    "license_expiry_date": "2025-12-31",
    "hire_date": "2023-01-15"
}
```

## Maintenance Management

### List Maintenance Records
```http
GET /api/maintenance/
Authorization: Bearer <access_token>
```

**Query Parameters**:
- `vehicle`: Filter by vehicle ID
- `status`: Filter by status (SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED)
- `maintenance_type`: Filter by type (ROUTINE, REPAIR, INSPECTION, OTHER)

**Response (200 OK)**:
```json
{
    "count": 50,
    "results": [
        {
            "id": 1,
            "vehicle": 1,
            "vehicle_details": {
                "id": 1,
                "license_plate": "ABC-123",
                "brand": "Toyota",
                "model": "Camry"
            },
            "maintenance_type": "ROUTINE",
            "status": "SCHEDULED",
            "description": "Regular oil change and inspection",
            "scheduled_date": "2024-02-15",
            "completed_date": null,
            "odometer_reading": 15000,
            "cost": "150.00",
            "service_provider": "AutoCare Services",
            "notes": "Check tire pressure",
            "days_until_scheduled": 10
        }
    ]
}
```

### Create Maintenance Record
```http
POST /api/maintenance/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "vehicle": 1,
    "maintenance_type": "ROUTINE",
    "description": "Regular oil change and inspection",
    "scheduled_date": "2024-02-15",
    "odometer_reading": 15000,
    "cost": "150.00",
    "service_provider": "AutoCare Services",
    "notes": "Check tire pressure"
}
```

## Emergency Management

### List Emergency Incidents
```http
GET /api/emergencies/
Authorization: Bearer <access_token>
```

**Response (200 OK)**:
```json
{
    "count": 5,
    "results": [
        {
            "id": 1,
            "incident_type": "ACCIDENT",
            "status": "REPORTED",
            "description": "Minor fender bender at intersection",
            "location": "Main St & 5th Ave",
            "reported_at": "2024-02-01T14:30:00Z",
            "resolved_at": null,
            "vehicle": {
                "id": 1,
                "license_plate": "ABC-123"
            },
            "driver": {
                "id": 1,
                "full_name": "John Doe"
            },
            "severity": "LOW"
        }
    ]
}
```

### Create Emergency Incident
```http
POST /api/emergencies/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "incident_type": "ACCIDENT",
    "description": "Minor fender bender at intersection",
    "location": "Main St & 5th Ave",
    "vehicle": 1,
    "driver": 1,
    "severity": "LOW"
}
```

## AI Screenshot Analysis

### Analyze Single Screenshot
```http
POST /api/screenshots/analyze/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

image: <file>
prompt: "Analyze this vehicle damage"
```

**Response (200 OK)**:
```json
{
    "analysis": "The image shows minor scratches on the front bumper...",
    "confidence": 0.85,
    "detected_issues": [
        "Front bumper damage",
        "Paint scratches"
    ],
    "recommended_actions": [
        "Schedule body shop appointment",
        "Document for insurance"
    ]
}
```

### Batch Analyze Screenshots
```http
POST /api/screenshots/batch-analyze/
Authorization: Bearer <access_token>
Content-Type: multipart/form-data

images: <file1>, <file2>, <file3>
```

### Generate Analysis Report
```http
POST /api/screenshots/generate-report/
Authorization: Bearer <access_token>
Content-Type: application/json

{
    "analysis_ids": [1, 2, 3],
    "report_type": "damage_assessment"
}
```

## Error Responses

### Standard Error Format
```json
{
    "error": "Error type",
    "message": "Detailed error message",
    "details": {
        "field": ["Field-specific error message"]
    }
}
```

### Common HTTP Status Codes

- **200 OK**: Request successful
- **201 Created**: Resource created successfully
- **400 Bad Request**: Invalid request data
- **401 Unauthorized**: Authentication required
- **403 Forbidden**: Insufficient permissions
- **404 Not Found**: Resource not found
- **500 Internal Server Error**: Server error

## Rate Limiting

API requests are limited to:
- **Authenticated users**: 1000 requests per hour
- **Anonymous users**: 100 requests per hour

## Pagination

List endpoints use cursor-based pagination:

```json
{
    "count": 100,
    "next": "http://localhost:8000/api/vehicles/?cursor=xyz",
    "previous": "http://localhost:8000/api/vehicles/?cursor=abc",
    "results": [...]
}
```

## Filtering and Search

Most list endpoints support filtering and search:

- **Filtering**: Use query parameters matching field names
- **Search**: Use `search` parameter for text search
- **Ordering**: Use `ordering` parameter (e.g., `ordering=-created_at`)

Example:
```
GET /api/vehicles/?status=AVAILABLE&search=Toyota&ordering=-year
```

## SDK and Client Libraries

### JavaScript (Lynx JS)
```javascript
import { FleetAPI } from 'lynx-fleet-client';

const api = new FleetAPI({
    baseURL: 'http://localhost:8000/api/',
    token: 'your-jwt-token'
});

const vehicles = await api.vehicles.list();
```

### Python
```python
import requests

class FleetAPI:
    def __init__(self, base_url, token):
        self.base_url = base_url
        self.headers = {'Authorization': f'Bearer {token}'}
    
    def get_vehicles(self):
        response = requests.get(f'{self.base_url}/vehicles/', headers=self.headers)
        return response.json()
```

## Webhooks (Future Feature)

The API will support webhooks for real-time notifications:

- Vehicle status changes
- Emergency incidents
- Maintenance due dates
- Driver assignments

---

For more information, see the [complete documentation](DOCUMENTATION.md) or contact the development team.