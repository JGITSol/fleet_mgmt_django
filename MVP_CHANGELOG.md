# 📄 MVP Sprint Changelog

Comprehensive audit of all code changes delivered during the MVP Polish Sprint (2026).

## 🗄 Backend (Django)

### Security & Middleware
- **[NEW]** `BotScannerFilterMiddleware`: Silently drops automated scanner probes (`/loginMsg.js`, `/cgi/`, etc.).
- **[FIX]** Removed all `print(f"DEBUG: ...")` leftover statements in `api/views.py`.

### Accounts & RBAC
- **[NEW]** `OneToOneField` link between `Driver` and `CustomUser`.
- **[NEW]** Scoped permissions logic in `UserRole.permissions` (JSONField).
- **[NEW]** `seed_roles_and_users` management command for idempotent fixture setup.
- **[NEW]** `ScopedPermission` class in `accounts/permissions.py`.
- **[NEW]** `/auth/switch-role/` endpoint for dev role simulation.

### API & Performance
- **[NEW]** Global `PageNumberPagination` enabled for all list endpoints.
- **[CLEANUP]** Removed 12 duplicate/redundant URL routing patterns.
- **[FIX]** Restored missing class headers for `Vehicle`, `Maintenance`, and `Emergency` detail views.

---

## 📱 Mobile Client (Flutter)

### Performance & UI
- **[OPTIMIZATION]** `FleetProvider`: Switched from sequential to parallel API fetching using `Future.wait()`.
- **[NEW]** Skeleton/Shimmer loading states in `DashboardScreen`.
- **[NEW]** `User.scopes` integration: Screen sections now show/hide based on exact role permissions.
- **[NEW]** Dev Role Switcher UI on the dashboard (visible to `testuser` and `admin`).

### Services & Logic
- **[NEW]** `ApiService._handleListResponse`: Gracefully handles both direct list and paginated (`results`) responses.
- **[NEW]** `AuthProvider.switchRole`: Integration with new backend role-switching logic.
- **[FIX]** `User` model updated to support `scopes` mapping from JWT/Profile.

---
*Verified & Validated — Sprint End 2026*
