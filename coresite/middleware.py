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
