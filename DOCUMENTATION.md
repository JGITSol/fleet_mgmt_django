# Car Fleet Management System - Complete Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Installation & Setup](#installation--setup)
4. [API Documentation](#api-documentation)
5. [Authentication](#authentication)
6. [Database Models](#database-models)
7. [Testing](#testing)
8. [Deployment](#deployment)
9. [Development Guidelines](#development-guidelines)
10. [Troubleshooting](#troubleshooting)

## Project Overview

The Car Fleet Management System is a comprehensive Django-based web application designed to manage vehicle fleets, maintenance schedules, drivers, and emergency incidents. The system provides both web interfaces and REST API endpoints for mobile app integration.

### Key Features

- **Vehicle Management**: Track vehicle details, status, assignments, and maintenance history
- **Driver Management**: Manage driver profiles, licenses, and vehicle assignments
- **Maintenance Scheduling**: Schedule and track maintenance activities with cost tracking
- **Emergency Response**: Handle emergency incidents and coordinate responses
- **JWT Authentication**: Secure API access with JSON Web Tokens
- **AI-Powered Analysis**: Screenshot analysis using OpenRouter/Google Generative AI
- **Mobile Integration**: REST API designed for Lynx JS mobile client
- **Role-Based Access**: Multi-level user permissions (Admin, Manager, Coordinator, Driver)

## Architecture

### Technology Stack

- **Backend**: Django 5.1.7 with Django REST Framework 3.16.0
- **Database**: SQLite (development), PostgreSQL (production ready)
- **Authentication**: JWT with djangorestframework-simplejwt 5.5.0
- **API Documentation**: drf-spectacular 0.28.0
- **Testing**: pytest-django 4.11.1 with coverage reporting
- **AI Integration**: Google Generative AI for image analysis
- **Frontend**: HTML templates with Bootstrap (web interface)

### Project Structure

```
CarFleetManagement/
├── accounts/           # User management and authentication
├── api/               # REST API endpoints and middleware
├── vehicles/          # Vehicle management
├── maintenance/       # Maintenance scheduling and tracking
├── emergency/         # Emergency incident management
├── static/           # Static files (CSS, JS, images)
├── templates/        # HTML templates
├── locale/           # Internationalization files
└── tests/            # Shared test utilities
```

## Installation & Setup

### Prerequisites

- Python 3.11+
- pip (Python package manager)
- Git

### Local Development Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd fleet_mgmt_django
   ```

2. **Create and activate virtual environment**:
   ```bash
   python -m venv venv
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment configuration**:
   ```bash
   # Windows PowerShell
   Copy-Item .env.example .env
   # Linux/Mac
   cp .env.example .env
   ```

5. **Database setup**:
   ```bash
   cd CarFleetManagement
   python manage.py migrate
   python manage.py createsuperuser
   ```

6. **Run development server**:
   ```bash
   python manage.py runserver
   ```

### Environment Variables

Configure the following variables in your `.env` file:

```env
DJANGO_SECRET_KEY=your-secret-key-here
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
DATABASE_URL=sqlite:///db.sqlite3
OPENROUTER_API_KEY=your-openrouter-key
GOOGLE_AI_API_KEY=your-google-ai-key
```

## API Documentation

### Base URL
- Development: `http://localhost:8000/api/`
- API Root: `/api/` - Returns available endpoints

### Authentication Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/auth/register/` | User registration |
| POST | `/api/auth/login/` | User login (returns JWT tokens) |
| POST | `/api/auth/logout/` | User logout |
| GET | `/api/auth/profile/` | Get user profile |
| POST | `/api/auth/validate-token/` | Validate JWT token |

### Vehicle Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/vehicles/` | List all vehicles |
| POST | `/api/vehicles/` | Create new vehicle |
| GET | `/api/vehicles/{id}/` | Get vehicle details |
| PUT | `/api/vehicles/{id}/` | Update vehicle |
| DELETE | `/api/vehicles/{id}/` | Delete vehicle |

### Driver Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/drivers/` | List all drivers |
| POST | `/api/drivers/` | Create new driver |
| GET | `/api/drivers/{id}/` | Get driver details |
| PUT | `/api/drivers/{id}/` | Update driver |
| DELETE | `/api/drivers/{id}/` | Delete driver |

### Maintenance Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/maintenance/` | List maintenance records |
| POST | `/api/maintenance/` | Create maintenance record |
| GET | `/api/maintenance/{id}/` | Get maintenance details |
| PUT | `/api/maintenance/{id}/` | Update maintenance record |
| DELETE | `/api/maintenance/{id}/` | Delete maintenance record |

### Emergency Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/emergencies/` | List emergency incidents |
| POST | `/api/emergencies/` | Create emergency incident |
| GET | `/api/emergencies/{id}/` | Get incident details |
| PUT | `/api/emergencies/{id}/` | Update incident |
| DELETE | `/api/emergencies/{id}/` | Delete incident |
| GET | `/api/emergencies/responses/` | List emergency responses |
| POST | `/api/emergencies/responses/` | Create emergency response |

### AI Analysis Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/screenshots/analyze/` | Analyze single screenshot |
| POST | `/api/screenshots/batch-analyze/` | Batch analyze screenshots |
| POST | `/api/screenshots/generate-report/` | Generate analysis report |

## Authentication

The system uses JWT (JSON Web Tokens) for API authentication:

### JWT Token Flow

1. **Login**: POST to `/api/auth/login/` with credentials
2. **Response**: Receive `access` and `refresh` tokens
3. **API Calls**: Include `Authorization: Bearer <access_token>` header
4. **Token Refresh**: Use refresh token to get new access token

### Example Authentication

```python
# Login
response = requests.post('/api/auth/login/', {
    'username': 'your_username',
    'password': 'your_password'
})
tokens = response.json()

# Use token in API calls
headers = {'Authorization': f'Bearer {tokens["access"]}'}
response = requests.get('/api/vehicles/', headers=headers)
```

### User Roles

- **Admin**: Full system access
- **Manager**: Fleet and user management
- **Coordinator**: Assignment and incident coordination
- **Driver**: Limited access to assigned vehicles
- **TestUser**: Development/testing purposes

## Database Models

### Core Models

#### CustomUser
Extended Django user model with role-based permissions:
- Role assignment (Admin, Manager, Coordinator, Driver, TestUser)
- Phone number and emergency contact
- Role-based property methods (`is_admin`, `is_manager`, etc.)

#### Vehicle
Comprehensive vehicle tracking:
- Basic info (brand, model, year, VIN, license plate)
- Technical specs (fuel type, transmission, vehicle type)
- Status tracking (Available, In Use, Maintenance, Out of Service)
- Service dates and insurance expiry

#### Driver
Driver management with license tracking:
- Personal information and contact details
- License number and expiry date
- Employment dates and status
- Vehicle assignments (many-to-many relationship)

#### Maintenance
Maintenance scheduling and tracking:
- Maintenance types (Routine, Repair, Inspection, Other)
- Status tracking (Scheduled, In Progress, Completed, Cancelled)
- Cost tracking and service provider information
- Odometer readings and completion dates

#### EmergencyIncident
Emergency incident management:
- Incident types (Accident, Breakdown, Medical, Theft, Other)
- Status tracking (Reported, Responding, Resolved, Closed)
- Location and description tracking
- Response coordination

## Testing

### Test Coverage

Current test coverage: **56%** (improved from 17%)

- Models: ~100% coverage
- Views/APIs: Moderate coverage with ongoing improvements
- Authentication: Complex test setup with patching system

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=CarFleetManagement --cov-report=html

# Run specific app tests
pytest CarFleetManagement/vehicles/tests/

# Run with verbose output
pytest -v -s
```

### Test Configuration

The project uses a sophisticated test patching system to handle JWT authentication in tests:

- **JWT Auth Patches**: Modify permission classes during testing
- **Test Fixtures**: Provide authenticated test clients
- **Database Setup**: Proper test database configuration

### Known Test Issues

1. **Authentication Complexity**: Multiple patch implementations for JWT testing
2. **Date Dependencies**: Some tests use hardcoded dates
3. **Fixture Scoping**: Django DB fixture scope mismatches

## Deployment

### Docker Deployment

```bash
# Build and run with Docker Compose
docker-compose up --build

# Production deployment
docker-compose -f docker-compose.prod.yml up -d
```

### Production Considerations

1. **Environment Variables**: Set secure values for production
2. **Database**: Use PostgreSQL instead of SQLite
3. **Static Files**: Configure proper static file serving
4. **Security**: Enable HTTPS and secure headers
5. **Monitoring**: Add logging and monitoring solutions

## Development Guidelines

### Code Style

- Follow PEP 8 Python style guidelines
- Use type hints where appropriate
- Write comprehensive docstrings
- Maintain test coverage above 80%

### API Design

- Follow REST conventions
- Use proper HTTP status codes
- Implement consistent error responses
- Version APIs when making breaking changes

### Security Best Practices

- Always use JWT authentication for API endpoints
- Validate and sanitize user input
- Implement proper permission checks
- Use HTTPS in production
- Keep dependencies updated

## Troubleshooting

### Common Issues

#### Authentication Errors
- **Issue**: JWT token not recognized
- **Solution**: Check token format and expiry, ensure proper Authorization header

#### Test Failures
- **Issue**: Authentication-related test failures
- **Solution**: Use the patched test runners or apply JWT patches

#### Database Issues
- **Issue**: Migration conflicts
- **Solution**: Reset migrations or use `--fake-initial` flag

#### Import Errors
- **Issue**: Module not found errors
- **Solution**: Check INSTALLED_APPS and Python path configuration

### Performance Optimization

1. **Database Queries**: Use `select_related` and `prefetch_related`
2. **Caching**: Implement Redis caching for frequently accessed data
3. **API Pagination**: Use pagination for large datasets
4. **Static Files**: Use CDN for static file delivery

### Debugging

- Enable Django debug toolbar for development
- Use logging for production debugging
- Monitor API response times and database queries
- Use Django's built-in error reporting

---

For additional support or questions, please refer to the project's issue tracker or contact the development team.