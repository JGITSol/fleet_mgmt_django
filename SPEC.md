# Fleet Management — System Specification

This document summarizes the core data models, database tables, and API endpoints for the Fleet Management project. It is intended to support code review, API design, and planning work to expand the codebase to industry standards (auditability, constraints, performance, and security).

## Contents
- Models and tables
- API endpoints (paths, methods, permissions)
- Suggested production hardening and extensions
- Linter / CI recommendations

---

## Models

Below are the primary Django models present in the codebase (as of the current workspace). For each model we list fields, types and relationships, plus notes and recommended improvements.

### Vehicle
- Table: vehicles_vehicle
- Purpose: represents a managed vehicle in the fleet.
- Fields:
  - id: AutoField (PK)
  - brand: CharField(max_length=100), default='Unknown'
  - model: CharField(max_length=100), default='Unknown'
  - year: IntegerField, default=2000
  - license_plate: CharField(max_length=20), unique=True
  - vin: CharField(max_length=17), unique=True, default='Unknown'
  - color: CharField(max_length=50), default='White'
  - fuel_type: CharField(max_length=20), choices=FuelType
  - transmission: CharField(max_length=20), choices=TransmissionType
  - vehicle_type: CharField(max_length=20), choices=VehicleType
  - mileage: IntegerField, default=0
  - last_service_date: DateField, null=True, blank=True
  - next_service_date: DateField, null=True, blank=True
  - insurance_expiry: DateField, null=True, blank=True
  - status: CharField(max_length=20), choices=Status, default=AVAILABLE
  - created_at: DateTimeField(auto_now_add=True)
  - updated_at: DateTimeField(auto_now=True)

Notes and suggestions:
- Add DB indexes on frequently queried fields (license_plate already unique; consider index on status, next_service_date for service scheduling queries).
- Consider adding soft-delete flag (is_active boolean) and an audit log for changes (who changed, when).
- Validate VIN format (checksum) and license plate patterns per region.
- Add constraints for year range (e.g., between 1886 and current_year + 1).

### Maintenance
- Table: maintenance_maintenance
- Purpose: records scheduled or completed maintenance actions for vehicles.
- Fields:
  - id: AutoField (PK)
  - vehicle_id: ForeignKey -> vehicles_vehicle (CASCADE)
  - maintenance_type: CharField(max_length=15), choices=MaintenanceType
  - status: CharField(max_length=15), choices=MaintenanceStatus
  - description: TextField
  - scheduled_date: DateField
  - completed_date: DateField, null=True, blank=True
  - odometer_reading: PositiveIntegerField
  - cost: DecimalField(max_digits=10, decimal_places=2)
  - service_provider: CharField(max_length=100)
  - notes: TextField, blank=True

Notes and suggestions:
- Add foreign-key index on vehicle_id (Django creates this by default).
- Add check constraints for non-negative cost and odometer readings (MinValueValidator used in model).
- Consider transactional guarantees when updating vehicle mileage together with maintenance records.

### EmergencyIncident
- Table: emergency_emergencyincident
- Purpose: record emergency incidents for vehicles (accidents, breakdowns, etc.).
- Fields:
  - id: AutoField (PK)
  - vehicle_id: ForeignKey -> vehicles_vehicle (CASCADE)
  - driver_id: ForeignKey -> accounts_driver (SET_NULL, null=True, blank=True)
  - reported_by_id: ForeignKey -> accounts_customuser (CASCADE)
  - emergency_type: CharField(max_length=20), choices=EmergencyType
  - status: CharField(max_length=20), choices=EmergencyStatus
  - location: CharField(max_length=255)
  - latitude: DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  - longitude: DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
  - description: TextField
  - reported_time: DateTimeField(auto_now_add=True)
  - resolved_time: DateTimeField(null=True, blank=True)

Notes and suggestions:
- Consider storing location as a GeoDjango PointField if geospatial queries or mapping are required.
- Add indexes on reported_time and status for query performance.

### EmergencyResponse
- Table: emergency_emergencyresponse
- Purpose: responses/actions taken for an EmergencyIncident.
- Fields:
  - id: AutoField (PK)
  - incident_id: ForeignKey -> emergency_emergencyincident (CASCADE)
  - responder_id: ForeignKey -> accounts_customuser (SET_NULL, null=True, blank=True)
  - response_time: DateTimeField(auto_now_add=True)
  - action_taken: TextField, null=True, blank=True
  - notes: TextField, blank=True

Notes:
- Use related_name 'responses' on EmergencyIncident for fast reverse lookups (already present).

### EmergencyContact
- Table: emergency_emergencycontact
- Purpose: user emergency contacts
- Fields: user (FK to CustomUser), name, phone_number, relationship

### UserRole
- Table: accounts_userrole
- Purpose: store roles (Admin, Manager, Driver, TestUser, Maintenance Staff)
- Fields: name (choice), description, permissions (JSONField)

Notes:
- ROLE_CHOICES defined as a ClassVar in model. For production, consider a stable role enumeration or a small table with canonical role rows seeded by migrations.

### CustomUser
- Table: accounts_customuser
- Purpose: extends Django's AbstractUser with a role FK and profile fields
- Fields: inherits Django user fields + role FK (UserRole), phone_number, emergency_contact

### Driver
- Table: accounts_driver
- Purpose: represent drivers linked to vehicles (ManyToMany assigned_vehicles)
- Fields: first_name, last_name, driver_license_number (unique), assigned_vehicles (M2M to Vehicle), phone_number, email

Notes:
- assigned_vehicles uses related_name 'drivers' on Vehicle model.

---

## API Endpoints

The project exposes both function/class-based DRF views and router-based ViewSets. The following is an extracted summary of endpoints and the corresponding view classes.

Top-level API router (rest framework DefaultRouter) registers these resources under `/api/` in the project routing:

- /users/  -> UserViewSet (router)
- /vehicles/ -> VehicleViewSet (router)
- /maintenance/ -> MaintenanceViewSet (router)
- /emergencies/ -> EmergencyIncidentViewSet (router)
- /drivers/ -> DriverViewSet (router)

Additionally, the analytic and screenshot endpoints are exposed:

- POST /analyze-screenshot/ -> AnalyzeScreenshotView
  - Content: multipart/form-data with `screenshot` file and optional `prompt` text
  - Response: JSON with analysis output (from external OpenRouter client)
  - Permissions: (in code, parser_classes specified; check auth/permission usage) — unauthenticated by default unless wrapped by auth middleware
  - Notes: writes screenshot to temp directory then calls external client; ensure anti-virus/size limits and cleanup.

- POST /batch-analyze-screenshots/ -> BatchAnalyzeScreenshotsView
  - Reads files from debug_screenshots directory, filters by language/theme/page, calls client for each
  - Risks: server-side file enumeration of project directory — restrict to controlled debug environments only and add auth/permission checks in prod.

- POST /generate-report/ -> GenerateReportView
  - Body: analysis_data JSON
  - Response: HTML content (report)
  - Notes: writes temp files, then invokes local report generator; ensure proper input validation and avoid XSS in generated HTML.

Also available in `CarFleetManagement/api/urls.py` (API app):

- /api/screenshots/analyze/ -> AnalyzeScreenshotView
- /api/screenshots/batch-analyze/ -> BatchAnalyzeScreenshotsView
- /api/screenshots/generate-report/ -> GenerateReportView

Auth endpoints in `CarFleetManagement/api/urls.py`:
- /api/auth/register/ -> RegisterView
- /api/auth/login/ -> LoginView
- /api/auth/logout/ -> LogoutView
- /api/auth/profile/ -> UserProfileView
- /api/auth/validate-token/ -> ValidateTokenView

Vehicle endpoints (class-based views):
- GET /api/vehicles/ -> VehicleListCreateAPIView (list)
- POST /api/vehicles/ -> VehicleListCreateAPIView (create)
- GET /api/vehicles/{pk}/ -> VehicleRetrieveUpdateDestroyAPIView (retrieve)
- PUT/PATCH /api/vehicles/{pk}/ -> VehicleRetrieveUpdateDestroyAPIView (update)
- DELETE /api/vehicles/{pk}/ -> VehicleRetrieveUpdateDestroyAPIView (destroy)

Maintenance endpoints (class-based views):
- GET /api/maintenance/ -> MaintenanceListCreateAPIView
- POST /api/maintenance/ -> MaintenanceListCreateAPIView
- GET/PUT/PATCH/DELETE /api/maintenance/{pk}/ -> MaintenanceRetrieveUpdateDestroyAPIView

Driver endpoints:
- GET /api/drivers/ -> DriverListCreateAPIView
- POST /api/drivers/ -> DriverListCreateAPIView
- GET /api/drivers/{pk}/ -> DriverRetrieveUpdateDestroyAPIView

Emergency endpoints:
- GET /api/emergencies/ -> EmergencyIncidentListCreateAPIView
- POST /api/emergencies/ -> EmergencyIncidentListCreateAPIView
- GET /api/emergencies/{pk}/ -> EmergencyIncidentRetrieveUpdateDestroyAPIView
- POST (form) to detail endpoints supported as legacy update with redirect behavior in HTML clients
- Emergency responses: /api/emergencies/responses/ and /api/emergencies/responses/{pk}/ -> create/list and retrieve/update/destroy

Special endpoints implemented in `api/urls.py` (top-level router):
- /emergencies/{incident_id}/response/create/ -> EmergencyResponseCreateView (from emergency.views)

---

## Permissions and Auth

- The API mixture uses JWTAuthentication for vehicle endpoints (explicit in `api/views.py`), and permission classes such as `IsAdminRole`, `IsAdminOrMaintenanceStaff`, and `IsAuthenticated` in different views.
- Important: Ensure permission checks are applied consistently across router ViewSets. Review all ViewSets to ensure authentication_classes and permission_classes are set.

## Recommended Production Hardening

1. Authentication & Authorization
   - Enforce authentication on all write endpoints by default. Use short-lived JWT tokens + refresh tokens and rotate secrets.
   - Implement role-based access control (RBAC) checks consistently. Prefer declarative DRF permission classes per ViewSet.

2. Input validation & sanitization
   - Validate uploaded files: size limits, file type checks, and store into secure object storage (S3) instead of local FS for scale.
   - Validate JSON payload shapes with serializers and disallow unknown fields.

3. Auditing & Data Governance
   - Add audit/log tables or an event stream for record changes (who, what, when). Use Django signals or a dedicated audit app.
   - Keep immutable changelogs for critical records (maintenance, emergency incident state transitions).

4. Database & Schema
   - Add DB-level constraints and indexes for performance and correctness.
   - Add FK ON DELETE rules consistent with business requirements (some are SET_NULL; confirm expected semantics).
   - Use migrations and schema review process; exclude migrations from strict linting.

5. Observability & Monitoring
   - Add structured logging (request IDs, user IDs), metrics (Prometheus), and distributed tracing.
   - Add health-check endpoints and readiness/liveness probes in container deployment.

6. Security
   - Sanitize report HTML output to prevent stored XSS if reports include user-supplied data.
   - Rate-limit heavy endpoints (screenshot analysis) and add quotas for external API calls.
   - Use secure storage for secrets and API keys (Azure Key Vault, AWS Secrets Manager or environment-based with restricted access).

## Linter & CI Recommendations

- Use `ruff` as primary linter with strict rules for Python code, but configure `pyproject.toml` to:
  - Exclude migrations and third-party assets from strict rules.
  - Per-file ignores for test utilities that legitimately use patterns flagged by security heuristics (S106 for test credentials, S603 for subprocess calls in dev scripts) — prefer explicit suppression comments for true issues.

- Add pre-commit hooks and a GitHub Actions workflow that:
  - Installs dependencies in a virtualenv, caches pip wheel cache and pip cache.
  - Runs `ruff --fix` (safe fixes) and `ruff check` as a CI job; fails on remaining errors.
  - Runs `isort` and `black` (if used) for formatting consistency.
  - Runs `pytest -q` and publishes test coverage and HTML reports (cache venv and pip downloads for speed).

Example CI jobs to include:
- lint (ruff, isort)
- tests (pytest) with coverage upload
- build-frontend (install bun/node + run build) if front-end artifacts required for integration tests

## Next steps (recommended small iterative roadmap)

1. Finalize `pyproject.toml` ruff configuration (exclude migrations, tests per-file-ignores for S106/S603 where appropriate).
2. Run `ruff --fix` across the repository, then re-run `ruff check` and fix remaining issues.
3. Run full test suite (pytest) and fix failing tests (address undefined names and fixtures used incorrectly).
4. Add pre-commit and CI jobs with caching for pip and test caches.
5. Add a migration audit and data retention policy; consider adding soft-delete and audit logs.

---

Document generated by automated analysis of code in d:/REPOS/fleet_mgmt_django. Review and adjust permissions, endpoint exposure, and data retention policies to match your organization's compliance requirements.
