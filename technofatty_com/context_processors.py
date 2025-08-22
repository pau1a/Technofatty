from django.conf import settings as django_settings


def settings(request):
    """Expose Django settings to templates.

    Allows templates to access site configuration values via the
    ``settings`` context variable.
    """
    return {"settings": django_settings}
