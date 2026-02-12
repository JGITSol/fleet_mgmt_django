# Car Fleet Management System

A comprehensive Django-based fleet management system with REST API, JWT authentication, and mobile app integration.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- pip
- Git

### 🎯 Automated Development Setup (Recommended)

```bash
# Clone and set up the project
git clone <repository-url>
cd fleet_mgmt_django

# Create and activate virtual environment
python -m venv venv
# Windows PowerShell:
.\venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Start development server with test credentials
python start_dev_server.py
```

### 🔧 Manual Development Setup

1. **Clone and setup environment**:
   ```bash
   git clone <repository-url>
   cd fleet_mgmt_django
   
   # Create virtual environment
   python -m venv venv
   
   # Activate virtual environment
   # Windows PowerShell:
   .\venv\Scripts\Activate.ps1
   # Linux/Mac:
   source venv/bin/activate
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup database and test users**:
   ```bash
   cd CarFleetManagement
   python manage.py migrate
   python manage.py setup_dev_users
   ```

4. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### 🔐 Development Test Credentials

The system comes with pre-configured test accounts for development:

| Role | Username | Password | Access Level |
|------|----------|----------|--------------|
| **Admin** | `admin` | `admin123!` | Full system access, Django admin |
| **Driver** | `testuser` | `user123!` | Limited access, driver functions |

### 🌐 Access Points

- **Web Interface:** http://localhost:8000/
- **Login Page:** http://localhost:8000/accounts/login/
- **Registration:** http://localhost:8000/accounts/register/
- **Admin Panel:** http://localhost:8000/admin/
- **API Root:** http://localhost:8000/api/
- **API Documentation:** http://localhost:8000/api/schema/swagger-ui/

### 🧪 Test Your Setup

```bash
# Test API credentials
python test_dev_credentials.py
```

## 🧪 Testing

### Run Tests
```bash
# Quick test run
.\run_tests.ps1

# Manual test execution
pytest -q

# With coverage report
pytest --cov=CarFleetManagement --cov-report=html
```

### Current Test Status
- **Coverage**: 56% (improved from 17%)
- **Total Tests**: 167 tests across all modules
- **Status**: Most core functionality tested, authentication tests require patches

## 🐳 Docker Deployment

```bash
# Development
docker-compose up --build

# Production (when available)
docker-compose -f docker-compose.prod.yml up -d
```

## 📋 Features

### Core Functionality
- **Vehicle Management**: Track vehicles, status, assignments, maintenance history
- **Driver Management**: Driver profiles, licenses, vehicle assignments
- **Maintenance Scheduling**: Schedule and track maintenance with cost tracking
- **Emergency Response**: Incident reporting and response coordination
- **User Roles**: Admin, Manager, Coordinator, Driver, TestUser permissions

### Technical Features
- **JWT Authentication**: Secure API access with token-based auth
- **REST API**: Complete API for mobile app integration
- **Dynamic Theming**: Premium design system with 10+ selectable color modes using `color-mix`.
- **AI Integration**: Screenshot analysis using Google AI
- **Internationalization**: Multi-language support (EN, PL, ES, DE, FR)
- **Comprehensive Testing**: pytest with coverage reporting
- **API Documentation**: Auto-generated with drf-spectacular

## 🏗️ Architecture

### Project Structure
```
CarFleetManagement/
├── accounts/           # User management & authentication
├── api/               # REST API endpoints & middleware
├── vehicles/          # Vehicle management
├── maintenance/       # Maintenance scheduling
├── emergency/         # Emergency incident management
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates (base_v3 standard)
└── tests/            # Shared test utilities
```

### Technology Stack
- **Backend**: Django 5.1.7 + Django REST Framework 3.16.0
- **Authentication**: JWT (djangorestframework-simplejwt 5.5.0)
- **Database**: SQLite (dev), PostgreSQL (production ready)
- **Frontend**: Modern Django Templates + Vanilla CSS (Custom Design System)
- **Testing**: pytest-django 4.11.1
- **AI**: Google Generative AI
- **Documentation**: drf-spectacular 0.28.0

## 🔐 Authentication

The system uses JWT authentication for API access:

```python
# Login to get tokens
POST /api/auth/login/
{
    "username": "your_username",
    "password": "your_password"
}

# Use access token in API calls
Authorization: Bearer <access_token>
```

## 📊 Current Status

### ✅ Completed
- Core models (Vehicle, Driver, Maintenance, Emergency)
- JWT authentication system
- REST API endpoints
- **Premium UI/UX overhaul** with `base_v3.html`
- **Dynamic Theme System** (10+ modes)
- Test infrastructure (56% coverage)
- Docker configuration
- AI screenshot analysis integration

### 🔄 In Progress
- Test stability improvements
- Authentication test patches
- API documentation completion
- Frontend enhancements

### 📋 Next Steps
1. **Stabilize Tests**: Fix authentication-related test failures
2. **Improve Coverage**: Increase test coverage to 80%+
3. **API Consistency**: Standardize error responses and status codes
4. **Documentation**: Complete API documentation with examples
5. **Production Setup**: Add production deployment guides
6. **Performance**: Optimize database queries and add caching

## 🛠️ Development

### Code Style
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Maintain comprehensive docstrings
- Write tests for new features

### Contributing
1. Fork the repository
2. Create a feature branch
3. Write tests for new functionality
4. Ensure all tests pass
5. Submit a pull request

## 📚 Documentation

- **Complete Documentation**: See [DOCUMENTATION.md](DOCUMENTATION.md)
- **Project Specification**: See [CurrentProjectSpecSheet.md](CurrentProjectSpecSheet.md)
- **Current State**: See [CurrentStateOfTheProject.md](CurrentStateOfTheProject.md)
- **API Schema**: Available at `/api/schema/` when running

## 🐛 Troubleshooting

### Common Issues

**Authentication Errors**:
- Ensure JWT tokens are properly formatted
- Check token expiry and refresh as needed

**Test Failures**:
- Use patched test runners for authentication tests
- Clear pytest cache: `pytest --cache-clear`

**Import Errors**:
- Verify virtual environment is activated
- Check INSTALLED_APPS configuration

### Getting Help
- Check the [DOCUMENTATION.md](DOCUMENTATION.md) for detailed guides
- Review test logs in `test_logs/` directory
- Check Django debug output for detailed error information

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
