# Deployment Guide - Car Fleet Management System

## Overview

This guide covers deployment options for the Car Fleet Management System, from development to production environments.

## Table of Contents

1. [Development Deployment](#development-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Production Deployment](#production-deployment)
4. [Environment Configuration](#environment-configuration)
5. [Database Setup](#database-setup)
6. [Security Configuration](#security-configuration)
7. [Monitoring and Logging](#monitoring-and-logging)
8. [Backup and Recovery](#backup-and-recovery)

## Development Deployment

### Local Development Setup

1. **Prerequisites**:
   ```bash
   # Required software
   - Python 3.11+
   - pip
   - Git
   - Node.js (for frontend assets)
   ```

2. **Quick Setup**:
   ```bash
   git clone <repository-url>
   cd fleet_mgmt_django
   python -m venv venv
   
   # Windows
   .\venv\Scripts\Activate.ps1
   # Linux/Mac
   source venv/bin/activate
   
   pip install -r requirements.txt
   Copy-Item .env.example .env  # Windows
   cp .env.example .env         # Linux/Mac
   
   cd CarFleetManagement
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

3. **Development Environment Variables**:
   ```env
   DJANGO_SECRET_KEY=dev-secret-key-change-in-production
   DJANGO_DEBUG=True
   DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

## Docker Deployment

### Development with Docker

1. **Docker Compose Setup**:
   ```yaml
   # docker-compose.yml
   version: '3.8'
   
   services:
     web:
       build: .
       ports:
         - "8000:8000"
       volumes:
         - .:/app
       environment:
         - DJANGO_DEBUG=True
       depends_on:
         - db
   
     db:
       image: postgres:15
       environment:
         POSTGRES_DB: fleet_management
         POSTGRES_USER: fleet_user
         POSTGRES_PASSWORD: fleet_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
   volumes:
     postgres_data:
   ```

2. **Run with Docker**:
   ```bash
   docker-compose up --build
   ```

### Production Docker Setup

1. **Multi-stage Dockerfile**:
   ```dockerfile
   # Dockerfile.prod
   FROM python:3.11-slim as builder
   
   WORKDIR /app
   COPY requirements.txt .
   RUN pip install --no-cache-dir -r requirements.txt
   
   FROM python:3.11-slim
   
   WORKDIR /app
   COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
   COPY . .
   
   RUN python manage.py collectstatic --noinput
   
   EXPOSE 8000
   CMD ["gunicorn", "--bind", "0.0.0.0:8000", "CarFleetManagement.wsgi:application"]
   ```

2. **Production Docker Compose**:
   ```yaml
   # docker-compose.prod.yml
   version: '3.8'
   
   services:
     web:
       build:
         context: .
         dockerfile: Dockerfile.prod
       ports:
         - "8000:8000"
       environment:
         - DJANGO_DEBUG=False
         - DATABASE_URL=postgresql://fleet_user:fleet_password@db:5432/fleet_management
       depends_on:
         - db
         - redis
   
     db:
       image: postgres:15
       environment:
         POSTGRES_DB: fleet_management
         POSTGRES_USER: fleet_user
         POSTGRES_PASSWORD: fleet_password
       volumes:
         - postgres_data:/var/lib/postgresql/data
   
     redis:
       image: redis:7-alpine
       volumes:
         - redis_data:/data
   
     nginx:
       image: nginx:alpine
       ports:
         - "80:80"
         - "443:443"
       volumes:
         - ./nginx.conf:/etc/nginx/nginx.conf
         - ./ssl:/etc/nginx/ssl
       depends_on:
         - web
   
   volumes:
     postgres_data:
     redis_data:
   ```

## Production Deployment

### Cloud Deployment Options

#### 1. AWS Deployment

**Using AWS ECS with Fargate**:

1. **Build and Push Docker Image**:
   ```bash
   # Build image
   docker build -f Dockerfile.prod -t fleet-management .
   
   # Tag for ECR
   docker tag fleet-management:latest 123456789012.dkr.ecr.us-west-2.amazonaws.com/fleet-management:latest
   
   # Push to ECR
   aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-west-2.amazonaws.com
   docker push 123456789012.dkr.ecr.us-west-2.amazonaws.com/fleet-management:latest
   ```

2. **ECS Task Definition**:
   ```json
   {
     "family": "fleet-management",
     "networkMode": "awsvpc",
     "requiresCompatibilities": ["FARGATE"],
     "cpu": "512",
     "memory": "1024",
     "executionRoleArn": "arn:aws:iam::123456789012:role/ecsTaskExecutionRole",
     "containerDefinitions": [
       {
         "name": "web",
         "image": "123456789012.dkr.ecr.us-west-2.amazonaws.com/fleet-management:latest",
         "portMappings": [
           {
             "containerPort": 8000,
             "protocol": "tcp"
           }
         ],
         "environment": [
           {
             "name": "DJANGO_DEBUG",
             "value": "False"
           }
         ],
         "secrets": [
           {
             "name": "DATABASE_URL",
             "valueFrom": "arn:aws:secretsmanager:us-west-2:123456789012:secret:fleet-db-url"
           }
         ]
       }
     ]
   }
   ```

#### 2. Google Cloud Platform

**Using Cloud Run**:

1. **Deploy to Cloud Run**:
   ```bash
   # Build and deploy
   gcloud run deploy fleet-management \
     --source . \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated \
     --set-env-vars DJANGO_DEBUG=False
   ```

#### 3. DigitalOcean App Platform

1. **App Spec**:
   ```yaml
   # .do/app.yaml
   name: fleet-management
   services:
   - name: web
     source_dir: /
     github:
       repo: your-username/fleet-management
       branch: main
     run_command: gunicorn --worker-tmp-dir /dev/shm CarFleetManagement.wsgi:application
     environment_slug: python
     instance_count: 1
     instance_size_slug: basic-xxs
     envs:
     - key: DJANGO_DEBUG
       value: "False"
     - key: DATABASE_URL
       value: ${db.DATABASE_URL}
   
   databases:
   - name: db
     engine: PG
     version: "15"
   ```

### Traditional Server Deployment

#### Ubuntu/Debian Server Setup

1. **System Dependencies**:
   ```bash
   sudo apt update
   sudo apt install python3.11 python3.11-venv python3-pip postgresql nginx supervisor
   ```

2. **Application Setup**:
   ```bash
   # Create application user
   sudo useradd --system --shell /bin/bash --home /opt/fleet-management fleet
   
   # Clone and setup application
   sudo -u fleet git clone <repository-url> /opt/fleet-management
   cd /opt/fleet-management
   sudo -u fleet python3.11 -m venv venv
   sudo -u fleet ./venv/bin/pip install -r requirements.txt
   ```

3. **Gunicorn Configuration**:
   ```ini
   # /etc/supervisor/conf.d/fleet-management.conf
   [program:fleet-management]
   command=/opt/fleet-management/venv/bin/gunicorn --workers 3 --bind unix:/opt/fleet-management/fleet.sock CarFleetManagement.wsgi:application
   directory=/opt/fleet-management/CarFleetManagement
   user=fleet
   autostart=true
   autorestart=true
   redirect_stderr=true
   stdout_logfile=/var/log/fleet-management.log
   ```

4. **Nginx Configuration**:
   ```nginx
   # /etc/nginx/sites-available/fleet-management
   server {
       listen 80;
       server_name your-domain.com;
   
       location /static/ {
           alias /opt/fleet-management/CarFleetManagement/staticfiles/;
       }
   
       location /media/ {
           alias /opt/fleet-management/CarFleetManagement/media/;
       }
   
       location / {
           proxy_pass http://unix:/opt/fleet-management/fleet.sock;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }
   }
   ```

## Environment Configuration

### Production Environment Variables

```env
# Security
DJANGO_SECRET_KEY=your-super-secret-key-here
DJANGO_DEBUG=False
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com

# Database
DATABASE_URL=postgresql://user:password@host:port/database

# Cache
REDIS_URL=redis://localhost:6379/0

# Email
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
EMAIL_HOST_USER=your-email@gmail.com
EMAIL_HOST_PASSWORD=your-app-password

# AI Services
OPENROUTER_API_KEY=your-openrouter-key
GOOGLE_AI_API_KEY=your-google-ai-key

# Storage (for production)
AWS_ACCESS_KEY_ID=your-aws-key
AWS_SECRET_ACCESS_KEY=your-aws-secret
AWS_STORAGE_BUCKET_NAME=your-bucket-name
AWS_S3_REGION_NAME=us-west-2

# Monitoring
SENTRY_DSN=your-sentry-dsn
```

### Security Settings

```python
# CarFleetManagement/settings/production.py
import os
from .base import *

# Security
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
SECURE_HSTS_SECONDS = 31536000
SECURE_REDIRECT_EXEMPT = []
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# CORS
CORS_ALLOW_CREDENTIALS = True
CORS_ALLOWED_ORIGINS = [
    "https://yourdomain.com",
    "https://www.yourdomain.com",
]
```

## Database Setup

### PostgreSQL Production Setup

1. **Install PostgreSQL**:
   ```bash
   sudo apt install postgresql postgresql-contrib
   ```

2. **Create Database and User**:
   ```sql
   sudo -u postgres psql
   
   CREATE DATABASE fleet_management;
   CREATE USER fleet_user WITH PASSWORD 'secure_password';
   GRANT ALL PRIVILEGES ON DATABASE fleet_management TO fleet_user;
   ALTER USER fleet_user CREATEDB;
   ```

3. **Configure Connection**:
   ```env
   DATABASE_URL=postgresql://fleet_user:secure_password@localhost:5432/fleet_management
   ```

### Database Migrations

```bash
# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic --noinput
```

## Security Configuration

### SSL/TLS Setup

1. **Let's Encrypt with Certbot**:
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
   ```

2. **Auto-renewal**:
   ```bash
   sudo crontab -e
   # Add line:
   0 12 * * * /usr/bin/certbot renew --quiet
   ```

### Firewall Configuration

```bash
# UFW setup
sudo ufw allow ssh
sudo ufw allow 'Nginx Full'
sudo ufw enable
```

## Monitoring and Logging

### Application Monitoring

1. **Sentry Integration**:
   ```python
   # settings/production.py
   import sentry_sdk
   from sentry_sdk.integrations.django import DjangoIntegration
   
   sentry_sdk.init(
       dsn=os.environ.get('SENTRY_DSN'),
       integrations=[DjangoIntegration()],
       traces_sample_rate=1.0,
       send_default_pii=True
   )
   ```

2. **Logging Configuration**:
   ```python
   LOGGING = {
       'version': 1,
       'disable_existing_loggers': False,
       'handlers': {
           'file': {
               'level': 'INFO',
               'class': 'logging.FileHandler',
               'filename': '/var/log/fleet-management/django.log',
           },
       },
       'loggers': {
           'django': {
               'handlers': ['file'],
               'level': 'INFO',
               'propagate': True,
           },
       },
   }
   ```

### System Monitoring

1. **Health Check Endpoint**:
   ```python
   # api/views.py
   from django.http import JsonResponse
   from django.db import connection
   
   def health_check(request):
       try:
           with connection.cursor() as cursor:
               cursor.execute("SELECT 1")
           return JsonResponse({"status": "healthy"})
       except Exception as e:
           return JsonResponse({"status": "unhealthy", "error": str(e)}, status=500)
   ```

2. **Monitoring with Prometheus**:
   ```python
   # Add to requirements.txt
   django-prometheus==2.3.1
   
   # Add to INSTALLED_APPS
   'django_prometheus',
   
   # Add to MIDDLEWARE (at the top)
   'django_prometheus.middleware.PrometheusBeforeMiddleware',
   'django_prometheus.middleware.PrometheusAfterMiddleware',
   ```

## Backup and Recovery

### Database Backup

1. **Automated Backup Script**:
   ```bash
   #!/bin/bash
   # backup.sh
   
   BACKUP_DIR="/opt/backups"
   DATE=$(date +%Y%m%d_%H%M%S)
   
   # Create backup
   pg_dump -h localhost -U fleet_user fleet_management > $BACKUP_DIR/fleet_backup_$DATE.sql
   
   # Compress backup
   gzip $BACKUP_DIR/fleet_backup_$DATE.sql
   
   # Remove backups older than 30 days
   find $BACKUP_DIR -name "fleet_backup_*.sql.gz" -mtime +30 -delete
   ```

2. **Cron Job for Backups**:
   ```bash
   # Add to crontab
   0 2 * * * /opt/scripts/backup.sh
   ```

### Recovery Procedures

1. **Database Recovery**:
   ```bash
   # Stop application
   sudo supervisorctl stop fleet-management
   
   # Restore database
   gunzip -c /opt/backups/fleet_backup_20240201_020000.sql.gz | psql -h localhost -U fleet_user fleet_management
   
   # Start application
   sudo supervisorctl start fleet-management
   ```

## Performance Optimization

### Caching Setup

1. **Redis Configuration**:
   ```python
   CACHES = {
       'default': {
           'BACKEND': 'django_redis.cache.RedisCache',
           'LOCATION': 'redis://127.0.0.1:6379/1',
           'OPTIONS': {
               'CLIENT_CLASS': 'django_redis.client.DefaultClient',
           }
       }
   }
   ```

2. **Database Optimization**:
   ```python
   # Database connection pooling
   DATABASES = {
       'default': {
           'ENGINE': 'django.db.backends.postgresql',
           'OPTIONS': {
               'MAX_CONNS': 20,
               'OPTIONS': {
                   'MAX_CONNS': 20,
               }
           }
       }
   }
   ```

### Static Files and CDN

```python
# AWS S3 for static files
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
STATICFILES_STORAGE = 'storages.backends.s3boto3.StaticS3Boto3Storage'

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = os.environ.get('AWS_STORAGE_BUCKET_NAME')
AWS_S3_REGION_NAME = os.environ.get('AWS_S3_REGION_NAME', 'us-west-2')
AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
```

## Troubleshooting

### Common Issues

1. **Static Files Not Loading**:
   ```bash
   python manage.py collectstatic --noinput
   sudo nginx -t && sudo systemctl reload nginx
   ```

2. **Database Connection Issues**:
   ```bash
   # Check PostgreSQL status
   sudo systemctl status postgresql
   
   # Test connection
   psql -h localhost -U fleet_user -d fleet_management
   ```

3. **Application Not Starting**:
   ```bash
   # Check logs
   sudo tail -f /var/log/fleet-management.log
   sudo supervisorctl status
   ```

### Performance Issues

1. **Database Query Optimization**:
   ```python
   # Enable query logging
   LOGGING['loggers']['django.db.backends'] = {
       'level': 'DEBUG',
       'handlers': ['console'],
   }
   ```

2. **Memory Usage**:
   ```bash
   # Monitor memory usage
   htop
   free -h
   ```

---

This deployment guide covers the essential aspects of deploying the Car Fleet Management System. For specific deployment scenarios or additional questions, consult the main documentation or contact the development team.