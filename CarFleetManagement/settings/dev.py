from .base import *
import socket

DEBUG = True

ALLOWED_HOSTS = ["localhost", "127.0.0.1", "0.0.0.0", "testserver"]

# Dynamically add the local IP to ALLOWED_HOSTS to simplify connection from mobile devices on the same network
try:
    hostname = socket.gethostname()
    local_ip = socket.gethostbyname(hostname)
    if local_ip not in ALLOWED_HOSTS:
        ALLOWED_HOSTS.append(local_ip)
except socket.error:
    pass

# Email settings for development (console backend)
EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"

# Development-friendly security (relaxed)
SECURE_SSL_REDIRECT = False
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
