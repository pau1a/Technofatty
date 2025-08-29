from django.conf import settings
from django.core.signing import BadSignature
from django.http import HttpResponse
from django.core.cache import cache
import re


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


PENDING_POST_QUEUE = []


class PostRateLimitMiddleware:
    """Rate limit and link throttle for community posts.

    - Limits posts to 1 per minute per user/IP.
    - Users with fewer than 3 approved posts may include only one link.
    - Unverified users' first posts are queued for moderation.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST" and request.path.startswith("/community"):
            user = getattr(request, "user", None)
            identifier = (
                getattr(user, "id", None)
                if getattr(user, "is_authenticated", False)
                else request.META.get("REMOTE_ADDR", "")
            )
            key = f"post:rate:{identifier}"
            if cache.get(key):
                return HttpResponse("Too many posts", status=429)
            cache.set(key, 1, 60)

            body = request.POST.get("body", "")
            if getattr(user, "approved_posts", 0) < 3:
                if len(re.findall(r"https?://", body)) > 1:
                    return HttpResponse("Too many links", status=400)

            if getattr(user, "approved_posts", 0) == 0 and not getattr(
                user, "is_verified", False
            ):
                PENDING_POST_QUEUE.append({
                    "user": user,
                    "title": request.POST.get("title", ""),
                    "body": body,
                })
                return HttpResponse("Post queued", status=202)

        return self.get_response(request)
