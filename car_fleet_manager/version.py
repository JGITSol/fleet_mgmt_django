"""Version information for Car Fleet Manager.

This module contains version information for the Car Fleet Manager application.
It follows Semantic Versioning 2.0.0 (https://semver.org/).
"""

__version__ = '0.1.1'

# Semantic versioning attributes
VERSION = __version__.split('.')
VERSION_MAJOR = int(VERSION[0])
VERSION_MINOR = int(VERSION[1])
VERSION_PATCH = int(VERSION[2]) if len(VERSION) > 2 else 0

# Build information (set automatically by CI/CD pipeline)
VERSION_BUILD = ''

# Full version display
VERSION_STRING = __version__
if VERSION_BUILD:
    VERSION_STRING += f"+{VERSION_BUILD}"

# Release information
RELEASE_STATUS = 'beta'  # Options: 'alpha', 'beta', 'rc', 'final'
RELEASE_DATE = '2024-06-20'  # Format: YYYY-MM-DD

# Version dictionary for easy access
VERSION_INFO = {
    'major': VERSION_MAJOR,
    'minor': VERSION_MINOR,
    'patch': VERSION_PATCH,
    'build': VERSION_BUILD,
    'status': RELEASE_STATUS,
    'date': RELEASE_DATE,
    'full': VERSION_STRING,
}