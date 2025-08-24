from django.conf import settings


def analytics_flags(request):
    return {
        'ANALYTICS_ENABLED': getattr(settings, 'ANALYTICS_ENABLED', False),
        'ANALYTICS_PROVIDER': getattr(settings, 'ANALYTICS_PROVIDER', ''),
        'ANALYTICS_SITE_ID': getattr(settings, 'ANALYTICS_SITE_ID', ''),
        'CONSENT_REQUIRED': getattr(settings, 'CONSENT_REQUIRED', True),
    }


def build_metadata(request):
    return {
        'build_branch': getattr(settings, 'BUILD_BRANCH', ''),
        'build_commit': getattr(settings, 'BUILD_COMMIT', ''),
        'build_datetime': getattr(settings, 'BUILD_DATETIME', ''),
        'show_build_banner': getattr(settings, 'SHOW_BUILD_BANNER', False),
    }
