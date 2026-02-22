# 🚛 Fleet Management Duo — Full-Stack Showcase

A complete, production-ready Fleet Management system featuring a **Django REST Framework** backend and a **Flutter** Android client.

## 🚀 feature Highlights

- **Granular RBAC**: Industry-standard Role-Based Access Control using scoped permissions (Admin, Manager, Coordinator, Driver, Maintenance).
- **Dynamic Role Switching**: Built-in developer tools to switch roles instantly for testing permission scopes and UI visibility.
- **Smart Data Isolation**: Drivers only see data related to their assigned vehicles or incidents they reported.
- **AI-Powered Diagnostics**: Screenshot analysis integration for vehicle status verification.
- **Modern UI/UX**: Shimmer loading skeletons, parallel data fetching, and polished Material 3 design.
- **Internationalization**: Full support for English and Polish (i18n & l10n).
- **Fleet Gallery**: Multi-media support (Images, Video, Sound) for maintenance and inspections.

## 🛠 Tech Stack

### Backend (Django)
- **Django REST Framework (DRF)**: Scalable API design.
- **SimpleJWT**: Secure token-based authentication.
- **drf-spectacular**: Automated OpenAPI 3.0 documentation.
- **Security Middleware**: Built-in protection against common bot scanner probes.
- **SQLite**: Portable database for easy showcase deployment.

### Mobile Client (Flutter)
- **Provider**: Robust state management.
- **Dio**: Advanced HTTP client with interceptors for JWT handling.
- **Intl**: Native localization management.
- **Custom Shimmer**: Premium loading experience.

## 🚦 Quick Start (Local Development)

### 1. Backend Setup
```bash
cd fleet_mgmt_django
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_roles_and_users
python manage.py runserver 0.0.0.0:8000
```
*Demo User: `demo_admin` / Password: `fleet2026!`*

### 2. Client Setup
1. Update `lib/services/api_service.dart` with your local IP.
2. Run `flutter pub get`.
3. Launch on Android Emulator or Physical Device.

## 📜 API Documentation
Access the interactive Swagger UI at:
`http://localhost:8000/api/schema/swagger-ui/`

---
*Created as part of the MVP Polish Sprint — 2026*
