from django.conf import settings


def analytics_flags(request):
    return {
        'ANALYTICS_ENABLED': getattr(settings, 'ANALYTICS_ENABLED', False),
        'ANALYTICS_PROVIDER': getattr(settings, 'ANALYTICS_PROVIDER', ''),
        'ANALYTICS_SITE_ID': getattr(settings, 'ANALYTICS_SITE_ID', ''),
        'CONSENT_REQUIRED': getattr(settings, 'CONSENT_REQUIRED', True),
    }
