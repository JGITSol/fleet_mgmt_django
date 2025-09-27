# URL ↔ Views ↔ Editable Fields Mapping

This document maps API endpoints (URLs) to the view classes and the serializer fields that are writable (editable) through each endpoint. It is generated from the repository serializer and view definitions and is intended to help reviewers and API consumers quickly see which model properties can be changed from each route.

Notes on inference:
- For serializers that declare explicit `read_only_fields`, any field not listed there is considered writeable.
- For serializers that use `fields = '__all__'`, writeable fields are inferred from the model (fields that are not auto-managed like `id`, `created_at`, `updated_at` are considered writeable unless the serializer documents otherwise).
- Nested/read-only nested fields are marked as read-only and cannot be directly written through the parent endpoint.

---

## Router-backed resources (DefaultRouter)

Base router paths (registered in `api/urls.py`): `/users/`, `/vehicles/`, `/maintenance/`, `/emergencies/`, `/drivers/`.

Each registered resource uses a ViewSet in `CarFleetManagement/api/views.py`. The ViewSets map standard REST actions to serializers listed in code.

### /users/  — UserViewSet
- Serializer: `CustomUserSerializer` (from `CarFleetManagement/api/serializers.py` / `CarFleetManagement/accounts/serializers.py`)
- Fields (serializer): `['id','username','email','first_name','last_name','role']` (read_only: `id`)
- Writable fields via endpoints (create/update): `username`, `email`, `first_name`, `last_name`, `role` (role expects a PK for a `UserRole`)
- Notes: Password management is handled by registration/login serializers — plain user endpoints do not accept `password` unless specifically implemented.

### /vehicles/  — VehicleViewSet
- Serializer: `VehicleSerializer` (`CarFleetManagement/vehicles/serializers.py`)
- Declared fields: id, vin, brand, model, year, vehicle_type, license_plate, mileage, status, fuel_type, transmission, color, last_service_date, next_service_date, insurance_expiry, created_at, updated_at, assigned_drivers (read_only), drivers (read_only), maintenance_records (read_only)
- read_only_fields: `id`, `created_at`, `updated_at`, and nested relations (assigned_drivers, drivers, maintenance_records)
- Writable fields via endpoints: `vin`, `brand`, `model`, `year`, `vehicle_type`, `license_plate`, `mileage`, `status`, `fuel_type`, `transmission`, `color`, `last_service_date`, `next_service_date`, `insurance_expiry`
- Notes: Driver assignment is represented as read-only nested data; driver assignment endpoints (`AssignDriverToVehicleAPIView` / `UnassignDriverFromVehicleAPIView`) manipulate relation via separate endpoints that accept `driver_id` in payload.

### /maintenance/  — MaintenanceViewSet
- Serializer: `MaintenanceSerializer` (`CarFleetManagement/maintenance/serializers.py`)
- Declared fields: id, vehicle, vehicle_details (read_only), maintenance_type, status, description, scheduled_date, completed_date, odometer_reading, cost, service_provider, notes, days_until_scheduled (read_only)
- read_only_fields: `id`, `vehicle_details`, `days_until_scheduled`
- Writable fields via endpoints: `vehicle` (FK id), `maintenance_type`, `status`, `description`, `scheduled_date`, `completed_date`, `odometer_reading`, `cost`, `service_provider`, `notes`
- Notes: `vehicle` is expected as vehicle PK in write payloads. The serializer computes `days_until_scheduled`; it is not writable.

### /emergencies/  — EmergencyIncidentViewSet
- Serializer: `EmergencyIncidentSerializer` (`CarFleetManagement/emergency/serializers.py`)
- Declared fields: `fields='__all__'` in serializer, but serializer sets `driver` as read-only nested and `reported_by` as read-only PK in code.
- Inferred model fields (from `CarFleetManagement/emergency/models.py`): vehicle (FK), driver (FK, nullable), reported_by (FK), emergency_type, status, location, latitude, longitude, description, reported_time, resolved_time
- Writable fields via list/create endpoints (inferred): `vehicle` (write via PK), `emergency_type`, `status`, `location`, `latitude`, `longitude`, `description`, `resolved_time` (some fields like `reported_by` are set in view (`serializer.save(reported_by=request.user)` in create) and may be read-only for clients)
- Notes: On create, the view attaches `reported_by=request.user` for form posts. `driver` is read-only nested representation; to change driver, update via incident update (if allowed) using driver PK (serializer read-only might prevent direct writes — check serializer if driver declared read_only=True)

### /drivers/  — DriverViewSet
- Serializer: `DriverSerializer` (`CarFleetManagement/accounts/serializers.py`)
- Declared fields: id, first_name, last_name, full_name (read_only), driver_license_number, assigned_vehicles (read_only nested), phone_number, email
- read_only_fields: `id`, `full_name`, `assigned_vehicles`
- Writable fields via endpoints: `first_name`, `last_name`, `driver_license_number`, `phone_number`, `email`
- Notes: `assigned_vehicles` is read-only nested; assignment should be done using dedicated endpoints or driver update accepting vehicle IDs if implemented.

---

## Hand-crafted class-based views and utilities (non-router)

These are defined in `CarFleetManagement/api/views.py` and `CarFleetManagement/api/urls.py`.

### POST /analyze-screenshot/  — AnalyzeScreenshotView
- Accepts multipart/form-data with file field `screenshot` and optional `prompt` text.
- Not a serializer-backed endpoint; payload fields accepted: `screenshot` (file), `prompt` (string)
- Writable input: the file and prompt only; server writes a temporary file and calls external client.

### POST /batch-analyze-screenshots/  — BatchAnalyzeScreenshotsView
- Accepts JSON/form with optional filters: `language`, `theme`, `page`, `prompt`.
- Not serializer-backed; no model fields are changed by this endpoint; it reads files from `debug_screenshots` and produces analysis.

### POST /generate-report/  — GenerateReportView
- Accepts JSON body with `analysis_data` (JSON serializable)
- Not serializer-backed; writes temp analysis file and returns generated HTML. No model fields are modified.

### POST /emergencies/<int:incident_id>/response/create/ — EmergencyResponseCreateView
- Implemented in `CarFleetManagement/emergency/views.py` and wired via `api/urls.py`.
- Expected writable payload: response fields per `EmergencyResponseSerializer` (fields='__all__', but serializer sets `responder` read_only=True), so create payload should include at least `incident` (or inferred from URL), `action_taken`, `notes`.
- The view likely binds `responder` to the current user when creating from authenticated context (check view implementation).

### Assign/Unassign Driver endpoints
- `AssignDriverToVehicleAPIView` (UpdateAPIView accepting `driver_id`): payload: `driver_id` (int)
- `UnassignDriverFromVehicleAPIView` (UpdateAPIView): payload: none (server sets vehicle.driver = None)

---

## Quick checklist for implementers / API consumers
- If you need to allow clients to change relationships (assign drivers to vehicles, add drivers to vehicles), implement explicit writeable fields or endpoints that accept lists of PKs.
- Prefer explicit nested write serializers only when needed. Current pattern: nested/read-only for related objects and separate endpoints for relationship mutation.
- For any endpoint that accepts file uploads (`/analyze-screenshot/`), enforce size limits and auth in production.

---

If you want, mogę teraz:
- (A) wygenerować szczegółową tabelę CSV/Markdown z kolumnami: endpoint, method, writeable fields (użyteczne do QA);
- (B) zaktualizować `SPEC.md` o te szczegółowe mapowania z linkami do plików;
- (C) dodać testy integracyjne (pytest) skeletony, które sprawdzą, czy pola są edytowalne według tej tabeli.
