# Environment Setup Guide

This guide explains how to set up the Django Car Fleet Management System for different environments.

## 🚀 Quick Start (Development)

1. **Set up development environment:**
   ```bash
   cd CarFleetManagement
   python manage.py migrate
   python ../setup_dev_credentials.py
   python manage.py runserver
   ```

2. **Access the application:**
   - Web UI: http://localhost:8000/
   - Admin Panel: http://localhost:8000/admin/
   - API Documentation: http://localhost:8000/api/schema/swagger-ui/

## 🔐 Test Credentials (Development Only)

### Admin User
- **Username:** `admin`
- **Password:** `admin123!`
- **Email:** `admin@fleetmanagement.dev`
- **Role:** Administrator (full access)

### Regular User
- **Username:** `testuser`
- **Password:** `user123!`
- **Email:** `user@fleetmanagement.dev`
- **Role:** Driver (limited access)

## 🏗️ Environment Configuration

### Development Environment (.env)
The development environment is configured in `CarFleetManagement/.env`:

```env
ENVIRONMENT=development
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1,0.0.0.0
# ... other development settings
```

**Features:**
- Debug mode enabled
- SQLite database
- Console email backend
- Relaxed security settings
- Test credentials included

### Production Environment (.env.production)
For production, copy `.env.production` to `.env.production.local` and configure:

```env
ENVIRONMENT=production
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgresql://username:password@localhost:5432/fleetmanagement_prod
# ... other production settings
```

**Features:**
- Debug mode disabled
- PostgreSQL database (recommended)
- SMTP email backend
- Strict security settings
- No test credentials

## 🔧 Environment Variables Reference

### Core Django Settings
| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `DJANGO_SECRET_KEY` | Dev key | Secure 50+ char key | Django secret key |
| `DJANGO_DEBUG` | `True` | `False` | Debug mode |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1` | `yourdomain.com` | Allowed hosts |
| `ENVIRONMENT` | `development` | `production` | Environment identifier |

### Database Settings
| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `DATABASE_URL` | `sqlite:///db.sqlite3` | `postgresql://...` | Database connection |

### Security Settings (Production Only)
| Variable | Default | Description |
|----------|---------|-------------|
| `SECURE_SSL_REDIRECT` | `True` | Force HTTPS |
| `SESSION_COOKIE_SECURE` | `True` | Secure session cookies |
| `CSRF_COOKIE_SECURE` | `True` | Secure CSRF cookies |
| `SECURE_HSTS_SECONDS` | `31536000` | HSTS max age |

### Email Settings
| Variable | Development | Production | Description |
|----------|-------------|------------|-------------|
| `EMAIL_BACKEND` | `console` | `smtp` | Email backend |
| `EMAIL_HOST` | `localhost` | `smtp.provider.com` | SMTP host |
| `EMAIL_PORT` | `1025` | `587` | SMTP port |

## 📦 Dependencies

### Required Python Packages
```bash
pip install django
pip install djangorestframework
pip install djangorestframework-simplejwt
pip install django-filter
pip install drf-spectacular
pip install python-dotenv
pip install dj-database-url  # For production PostgreSQL
```

### Production Additional Requirements
```bash
pip install psycopg2-binary  # PostgreSQL adapter
pip install gunicorn        # WSGI server
pip install redis           # Caching (optional)
```

## 🚀 Deployment Checklist

### Pre-Production Setup
- [ ] Copy `.env.production` to `.env.production.local`
- [ ] Generate secure `DJANGO_SECRET_KEY` (50+ characters)
- [ ] Set up PostgreSQL database
- [ ] Configure SMTP email settings
- [ ] Set up SSL certificates
- [ ] Configure domain and DNS

### Production Deployment
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DJANGO_DEBUG=False`
- [ ] Run `python manage.py collectstatic`
- [ ] Run `python manage.py migrate`
- [ ] Create superuser: `python manage.py createsuperuser`
- [ ] Set up web server (nginx/Apache)
- [ ] Configure WSGI server (gunicorn)
- [ ] Set up monitoring and logging

### Security Verification
- [ ] Verify HTTPS is working
- [ ] Check security headers
- [ ] Test authentication flows
- [ ] Verify database security
- [ ] Review file permissions

## 🔍 Troubleshooting

### Common Development Issues

**Database Issues:**
```bash
# Reset database
rm db.sqlite3
python manage.py migrate
python ../setup_dev_credentials.py
```

**Static Files Issues:**
```bash
python manage.py collectstatic --clear
```

**Permission Issues:**
```bash
# Recreate test users
python ../setup_dev_credentials.py
```

### Common Production Issues

**Static Files Not Loading:**
- Check `STATIC_ROOT` and `STATIC_URL` settings
- Run `python manage.py collectstatic`
- Verify web server static file configuration

**Database Connection Issues:**
- Verify `DATABASE_URL` format
- Check database server status
- Verify credentials and permissions

**Email Not Working:**
- Check SMTP settings
- Verify email provider configuration
- Test with development console backend first

## 📚 Additional Resources

- [Django Deployment Checklist](https://docs.djangoproject.com/en/stable/howto/deployment/checklist/)
- [Django Security Best Practices](https://docs.djangoproject.com/en/stable/topics/security/)
- [PostgreSQL Setup Guide](https://www.postgresql.org/docs/current/tutorial-start.html)

## ⚠️ Security Notes

1. **Never commit `.env.production.local` to version control**
2. **Use strong, unique passwords in production**
3. **Regularly update dependencies**
4. **Monitor logs for security issues**
5. **Use HTTPS in production**
6. **Regularly backup your database**