import logging
from django.core.cache import cache
from django.core.cache.backends.base import CacheKeyWarning
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render

from .forms import SignupForm
from .models import Subscriber, SiteSettings

logger = logging.getLogger(__name__)


def home(request):
    """Renders the homepage with site settings and a signup form."""
    settings = SiteSettings.objects.first()
    signup_form = SignupForm()
    return render(request, 'coresite/homepage.html', {
        'settings': settings,
        'signup_form': signup_form,
    })


def _get_client_ip(request):
    """Get the client's real IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _increment_ip_counter(ip_address, limit=5, timeout=3600):
    """
    Increments and checks a rate-limiting counter for a given IP.
    Returns True if the limit is exceeded, False otherwise.
    """
    # UNCERTAINTY: This assumes a cache backend is configured.
    # If not, it will fail gracefully but rate limiting will be disabled.
    try:
        cache_key = f"signup_attempt_ip_{ip_address}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=timeout)
        if count > limit:
            return True
    except (CacheKeyWarning, AttributeError, ImportError):
        logger.warning(
            f"Cache not configured or unavailable, skipping rate limit for IP {ip_address}."
        )
    return False


@require_POST
def signup_view(request):
    """Handles newsletter signup form submissions."""
    is_xhr = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    ip_address = _get_client_ip(request)

    if _increment_ip_counter(ip_address):
        message = "You have made too many requests. Please try again later."
        if is_xhr:
            return JsonResponse({'success': False, 'message': message}, status=429)
        messages.error(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))

    form = SignupForm(request.POST)

    if form.is_valid():
        email = form.cleaned_data['email']
        subscriber, created = Subscriber.objects.get_or_create(
            email__iexact=email,
            defaults={
                'email': email,
                'name': form.cleaned_data.get('name', ''),
                'company': form.cleaned_data.get('company', ''),
                'consent': form.cleaned_data['consent'],
                'ip_address': ip_address,
                'mailchimp_status': 'queued',
            }
        )
        if not created:
            subscriber.mailchimp_status = 'queued'
            subscriber.save(update_fields=['mailchimp_status'])

        message = "Thanks for subscribing! Please check your email to confirm."
        if is_xhr:
            return JsonResponse({'success': True, 'message': message})
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        error_message = next((iter(v) for k, v in form.errors.items()), "Please correct the errors below.")
        if is_xhr:
            return JsonResponse({'success': False, 'message': error_message, 'errors': form.errors}, status=400)
        messages.error(request, error_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))