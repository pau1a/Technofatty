import logging
from datetime import datetime

from django.core.cache import cache
from django.core.cache.backends.base import CacheKeyWarning
from django.http import JsonResponse, HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.shortcuts import render

from .forms import SignupForm
from .models import Subscriber, SiteSettings, SiteImage

logger = logging.getLogger(__name__)


def home(request):
    """Renders the homepage with site settings, resources, images and a signup form."""
    resources = [
        {"title": "AI for Marketing", "blurb": "Boost campaigns with smarter targeting and automation.", "url": "/resources/marketing/"},
        {"title": "AI in Operations", "blurb": "Cut waste and streamline workflows with predictive AI.", "url": "/resources/operations/"},
        {"title": "AI Case Studies", "blurb": "See how real businesses turned AI into growth.", "url": "/case-studies/"},
    ]
    settings = SiteSettings.objects.first()  # uncertainty: ensure SiteSettings exists
    signup_form = SignupForm()
    images = {img.key.replace("-", "_"): img for img in SiteImage.objects.all()}
    context = {
        "settings": settings,
        "signup_form": signup_form,
        "site_images": images,
        "is_homepage": True,
        "now": datetime.now(),
        "resources": resources,
    }
    return render(request, "coresite/homepage.html", context)


def _get_client_ip(request):
    """Get the client's real IP address from the request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def _increment_ip_counter(ip_address, limit=5, timeout=3600):
    """
    Increments and checks a rate-limiting counter for a given IP.
    Returns True if the limit is exceeded, False otherwise.
    """
    try:
        cache_key = f"signup_attempt_ip_{ip_address}"
        count = cache.get(cache_key, 0) + 1
        cache.set(cache_key, count, timeout=timeout)
        if count > limit:
            return True
    except Exception:
        logger.warning(f"Cache not configured or unavailable, skipping rate limit for IP {ip_address}.")
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
        # find existing subscriber case-insensitively, or create
        subscriber = Subscriber.objects.filter(email__iexact=email).first()
        if not subscriber:
            subscriber = Subscriber.objects.create(
                email=email,
                name=form.cleaned_data.get('name', ''),
                company=form.cleaned_data.get('company', ''),
                consent=form.cleaned_data.get('consent', False),
                ip_address=ip_address,
                mailchimp_status='queued',
            )
            created = True
        else:
            created = False
            subscriber.mailchimp_status = 'queued'
            subscriber.save(update_fields=['mailchimp_status'])

        # increment rate counter only on valid attempt (best-effort)
        try:
            cache_key = f"signup_attempt_ip_{ip_address}"
            count = cache.get(cache_key, 0) + 1
            cache.set(cache_key, count, 3600)
        except Exception:
            logger.debug("Cache unavailable; skipped increment after valid signup.")

        message = "Thanks for subscribing! Please check your email to confirm."
        if is_xhr:
            return JsonResponse({'success': True, 'message': message})
        messages.success(request, message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
    else:
        # extract a single human readable error if available
        first_error = None
        for v in form.errors.values():
            if v:
                first_error = v[0]
                break
        error_message = first_error or "Please correct the errors below."
        if is_xhr:
            return JsonResponse({'success': False, 'message': error_message, 'errors': form.errors}, status=400)
        messages.error(request, error_message)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER', '/'))
