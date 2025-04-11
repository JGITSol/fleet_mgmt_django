"""
Test settings for the Car Fleet Management project.
These settings are used when running tests.
"""
from .settings import *

# Use an in-memory SQLite database for faster tests
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}

# Disable migrations for tests to speed up test runs
class DisableMigrations:
    def __contains__(self, item):
        return True

    def __getitem__(self, item):
        return None

MIGRATION_MODULES = DisableMigrations()

# Disable password hashing to speed up user creation in tests
PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.MD5PasswordHasher',
]

# Disable debug mode for tests
DEBUG = False

# Disable logging during tests
LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
}
