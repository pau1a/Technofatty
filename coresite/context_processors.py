from django.conf import settings
from django.core import signing
from functools import lru_cache


@lru_cache()
def _build_nav_links():
    return [
        {
            "label": "Knowledge",
            "url": "knowledge",
            "locations": ["header", "footer"],
            "order": 1,
        },
        {
            "label": "Tools",
            "url": "tools",
            "locations": ["header", "footer"],
            "order": 2,
        },
        {
            "label": "Case Studies",
            "url": "case_studies",
            "locations": ["header", "footer"],
            "order": 3,
        },
        {
            "label": "Community",
            "url": "community",
            "locations": ["header", "footer"],
            "order": 4,
            "requires_auth": True,
            "alt_url": "join",
            "sr_id": "community-locked",
            "sr_text": "Available after you join.",
        },
        {
            "label": "Blog",
            "url": "blog",
            "locations": ["header", "footer"],
            "order": 5,
        },
        {
            "label": "Account",
            "url": "account",
            "locations": ["footer"],
            "order": 6,
            "requires_auth": True,
        },
        {
            "label": "Join Free",
            "url": "join",
            "locations": ["footer"],
            "order": 7,
            "requires_anon": True,
        },
        {
            "label": "About",
            "url": "about",
            "locations": ["footer"],
            "order": 8,
        },
        {
            "label": "Contact",
            "url": "contact",
            "locations": ["footer"],
            "order": 9,
        },
        {
            "label": "Support",
            "url": "support",
            "locations": ["footer"],
            "order": 10,
        },
        {
            "label": "Legal",
            "url": "legal",
            "locations": ["footer"],
            "order": 11,
        },
    ]


# Expose the cached structure for import in tests and other modules
NAV_LINKS = _build_nav_links()


def analytics_flags(request):
    """Expose analytics configuration and consent flags."""

    consent_granted = getattr(request, "CONSENT_GRANTED", False)

    signer = signing.get_cookie_signer()

    return {
        "ANALYTICS_ENABLED": getattr(settings, "ANALYTICS_ENABLED", False),
        "ANALYTICS_PROVIDER": getattr(settings, "ANALYTICS_PROVIDER", ""),
        "ANALYTICS_SITE_ID": getattr(settings, "ANALYTICS_SITE_ID", ""),
        "CONSENT_REQUIRED": getattr(settings, "CONSENT_REQUIRED", True),
        "CONSENT_GRANTED": consent_granted,
        "CONSENT_COOKIE_NAME": getattr(
            settings, "CONSENT_COOKIE_NAME", "tf_consent"
        ),
        "CONSENT_COOKIE_MAX_AGE": getattr(
            settings, "CONSENT_COOKIE_MAX_AGE", 60 * 60 * 24 * 365
        ),
        "CONSENT_COOKIE_SAMESITE": getattr(
            settings, "CONSENT_COOKIE_SAMESITE", "Lax"
        ),
        "CONSENT_COOKIE_SECURE": getattr(
            settings, "CONSENT_COOKIE_SECURE", not settings.DEBUG
        ),
        "CONSENT_COOKIE_HTTPONLY": getattr(
            settings, "CONSENT_COOKIE_HTTPONLY", True
        ),
        "CONSENT_ACCEPT_TOKEN": signer.sign("true"),
        "CONSENT_DECLINE_TOKEN": signer.sign("false"),
    }


def build_metadata(request):
    return {
        'build_branch': getattr(settings, 'BUILD_BRANCH', ''),
        'build_commit': getattr(settings, 'BUILD_COMMIT', ''),
        'build_datetime': getattr(settings, 'BUILD_DATETIME', ''),
        'show_build_banner': getattr(settings, 'SHOW_BUILD_BANNER', False),
    }


def nav_links(request):
    return {"nav_links": NAV_LINKS}
