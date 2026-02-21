# Flutter App Full Specification: Fleet Management

This specification is for a coding agent to generate a full-featured Flutter/Dart Android application that integrates with a Django REST Framework backend.

## Project Overview
The app is a Fleet Management tool allowing users to manage vehicles, track maintenance, report emergencies, and coordinate drivers.

## Core Technical Requirements
- **Framework**: Flutter (latest stable)
- **Language**: Dart
- **State Management**: Provider or Riverpod (recommended)
- **API Client**: Dio or http
- **Authentication**: JWT (Access + Refresh tokens)
- **Localization**: Localizations (i18n) support

---

## Data Models (Dart)

### Vehicle
```dart
class Vehicle {
  final int id;
  final String brand;
  final String model;
  final int year;
  final String licensePlate;
  final String vin;
  final String color;
  final String fuelType; // DIESEL, PETROL, HYBRID, ELECTRIC
  final String transmission; // MANUAL, AUTOMATIC
  final String vehicleType; // TRUCK, VAN, SUV, PICKUP
  final int mileage;
  final DateTime? lastServiceDate;
  final DateTime? nextServiceDate;
  final DateTime? insuranceExpiry;
  final String status; // AVAILABLE, IN_USE, MAINTENANCE, OUT_OF_SERVICE
  final List<DriverNested> assignedDrivers;
  final DateTime createdAt;
  final DateTime updatedAt;
}

class DriverNested {
  final int id;
  final String fullName;
}

class VehicleMedia {
  final int id;
  final int vehicleId;
  final String mediaType; // IMAGE, VIDEO, SOUND
  final String fileUrl;
  final String title;
  final String description;
  final DateTime createdAt;
}
```

### Maintenance
```dart
class Maintenance {
  final int id;
  final int vehicleId;
  final String maintenanceType; // ROUTINE, REPAIR, INSPECTION, OTHER
  final String status; // SCHEDULED, IN_PROGRESS, COMPLETED, CANCELLED
  final String description;
  final DateTime scheduledDate;
  final DateTime? completedDate;
  final int odometerReading;
  final double cost;
  final String serviceProvider;
  final String? notes;
  final int? daysUntilScheduled;
}
```

### Driver
```dart
class Driver {
  final int id;
  final String firstName;
  final String lastName;
  final String fullName;
  final String driverLicenseNumber;
  final String phoneNumber;
  final String email;
  final List<VehicleNested> assignedVehicles;
  final String status; // active, inactive
  final DateTime? licenseExpiryDate;
}

class VehicleNested {
  final int id;
  final String licensePlate;
}
```

### Emergency Incident & Response
```dart
class EmergencyIncident {
  final int id;
  final int vehicleId;
  final int? driverId;
  final int reportedBy;
  final String emergencyType; // ACCIDENT, BREAKDOWN, MEDICAL, THEFT, OTHER
  final String status; // REPORTED, RESPONDING, RESOLVED, CLOSED
  final String location;
  final double? latitude;
  final double? longitude;
  final String description;
  final DateTime reportedTime;
  final DateTime? resolvedTime;
}

class EmergencyResponse {
  final int id;
  final int incidentId;
  final int? responderId;
  final DateTime responseTime;
  final String? actionTaken;
  final String notes;
}
```

---

## API Endpoints (`/api/`)

### Authentication
- `POST /auth/login/`: Returns `{user: {id, username, email, role: {name, ...}}, access: "...", refresh: "..."}`
- `POST /auth/register/`: Register user (Role: user/safe default).
- `GET /auth/profile/`: Fetch current user info and roles.

### Resources
- `/vehicles/`: List/Create (Admin only).
- `/maintenance/`: List/Create (Admin/Maintenance Staff).
- `/drivers/`: List/Create (Authenticated).
- `/emergencies/`: List/Report (Authenticated).
- `/emergencies/responses/`: Create/List (Authenticated).
- `/vehicles/media/`: List/Upload Gallery Items (Authenticated). Use `?vehicle=ID` to filter.

---

## Theming System
The app must support the 10+ premium modes described in `COLOR_MODES.md`.

| Theme Name | Style |
|------------|-------|
| Classic Blue | Harmony & Trust |
| Solarized | Modern & Clean |
| Emerald | Fresh & Grounding |
| Rose Quartz | Elegant & Soft |
| Papyrus | Classic & Literary |
| *And variants* | Light & Dark for each |

---

## UI Components & Screens
1. **Login**: JWT Auth with role detection.
2. **Dashboard**: Stats and service alerts (service due logic: `nextServiceDate <= today`).
3. **Emergency**: One-tap reporting with automatic GPS capture.
4. **Settings**: Theme switcher (persisted locally).
