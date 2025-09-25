from rest_framework_simplejwt.authentication import JWTAuthentication
from django.utils.deprecation import MiddlewareMixin


class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware that attempts to authenticate users from the Authorization
    header using JWTAuthentication and sets request.user and request._cached_user.

    Behaviour:
    - If request already has an authenticated user, leave it alone.
    - If Authorization header contains a Bearer token, call
      JWTAuthentication().authenticate(request) and, on success, set both
      request.user and request._cached_user to the authenticated user.
    - Any exception from the authentication backend is swallowed and the
      request.user remains as-is (typically AnonymousUser).
    """

    def process_request(self, request):
        # If request already has an authenticated user (e.g., session auth), do nothing
        if getattr(request, 'user', None) and getattr(request.user, 'is_authenticated', False):
            return None

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if not auth_header or not auth_header.startswith('Bearer '):
            return None

        jwt_auth = JWTAuthentication()
        try:
            user_auth = jwt_auth.authenticate(request)
            if user_auth is not None:
                user, token = user_auth
                request.user = user
                # Some code expects _cached_user attribute to be present (tests)
                # Best-effort: set cached user attribute so code/tests that check it succeed
                request._cached_user = user
        except Exception:
            # Do not propagate authentication errors; leave request.user as-is
            return None

        return None
