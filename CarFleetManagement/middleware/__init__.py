"""
Security middleware for filtering bot scanner probes.

Internet-facing Django servers receive constant automated probes from
vulnerability scanners looking for common CMS/router endpoints. These
generate noisy 404 log entries that obscure real issues.

This middleware intercepts known scanner paths and returns a minimal
404 response without running Django's full URL resolution or error
rendering.
"""

from django.http import HttpResponseNotFound

# Paths and prefixes commonly probed by automated scanners
SCANNER_PATHS = frozenset([
    '/loginMsg.js',
    '/login.action',
    '/.env',
    '/wp-admin/',
    '/wp-login.php',
    '/administrator/',
    '/admin.php',
    '/xmlrpc.php',
    '/config.json',
    '/actuator',
    '/solr/',
    '/console/',
    '/.git/config',
    '/telescope/requests',
])

SCANNER_PREFIXES = (
    '/cgi/',
    '/cgi-bin/',
    '/wp-',
    '/.well-known/security.txt',
)


class BotScannerFilterMiddleware:
    """Return a silent 404 for known bot scanner paths.

    This prevents Django from logging verbose 404 errors and rendering
    full HTML error pages for requests that are clearly not from
    legitimate users.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path

        if path in SCANNER_PATHS or any(path.startswith(p) for p in SCANNER_PREFIXES):
            return HttpResponseNotFound(b'', content_type='text/plain')

        return self.get_response(request)
