from django.conf import settings
from django.core.signing import BadSignature


class ConsentMiddleware:
    """Attach CONSENT_GRANTED flag to each request."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        consent_granted = False
        try:
            consent_granted = (
                request.get_signed_cookie(settings.CONSENT_COOKIE_NAME) == "true"
            )
        except (KeyError, BadSignature):
            consent_granted = False
        request.CONSENT_GRANTED = consent_granted
        response = self.get_response(request)
        return response


class StaticCacheControlMiddleware:
    """Add long-lived Cache-Control headers for static assets.

    Only relevant when Django serves static files (e.g., in DEBUG).
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith(settings.STATIC_URL):
            response.headers.setdefault(
                "Cache-Control", "public, max-age=31536000, immutable"
            )
        return response
