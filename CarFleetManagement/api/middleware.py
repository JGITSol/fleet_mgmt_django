from rest_framework_simplejwt.authentication import JWTAuthentication


class JWTAuthMiddleware:
    """Middleware that attempts to authenticate users from the Authorization
    header using JWTAuthentication and sets request.user accordingly.

    This helps HTML views in tests that set JWT Authorization headers to work
    with Django's request.user-based decorators and template context.
    """
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # If request already has a user (session auth), keep it.
        if getattr(request, 'user', None) and request.user.is_authenticated:
            return self.get_response(request)

        auth = request.META.get('HTTP_AUTHORIZATION')
        if auth and auth.startswith('Bearer '):
            jwt_auth = JWTAuthentication()
            try:
                user_auth_tuple = jwt_auth.authenticate(request)
                if user_auth_tuple is not None:
                    user, token = user_auth_tuple
                    # Set both request.user and request._cached_user to be safe
                    request.user = user
                    request._cached_user = user
            except Exception:
                # Do not raise; middleware should be best-effort only
                pass

        return self.get_response(request)
from django.utils.deprecation import MiddlewareMixin


class JWTAuthMiddleware(MiddlewareMixin):
    """Middleware that authenticates a request using JWT from the Authorization header

    This lets Django's regular view auth (e.g., LoginRequiredMixin) see the user
    when tests or clients send a Bearer token instead of a session cookie.
    """
    def process_request(self, request):
        header = request.META.get('HTTP_AUTHORIZATION', '')
        if not header or not header.startswith('Bearer '):
            return None

        token = header.split(' ', 1)[1]
        auth = JWTAuthentication()
        try:
            # DRF's JWTAuthentication provides get_validated_token and get_user
            validated = auth.get_validated_token(token)
            user = auth.get_user(validated)
            request.user = user
        except Exception:
            # Leave request.user as-is (AnonymousUser) on failure
            return None
