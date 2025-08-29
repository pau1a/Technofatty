import hashlib
import time

from django.conf import settings
from django.core.cache import cache
from django.http import HttpResponseNotAllowed
from django.shortcuts import render

from .copy import get_copy
from .forms import NewsletterSubscribeForm
from .providers import Result, get_provider
from .utils import log_newsletter_event


def _render_noindex(request, template, context):
    """Render a template with noindex header."""
    response = render(request, template, context)
    response["X-Robots-Tag"] = "noindex"
    return response


def newsletter_form(request):
    """Render newsletter signup form and handle submissions."""
    copy = get_copy()
    if request.method == "GET":
        form = NewsletterSubscribeForm()
        context = {
            "form": form,
            "copy": copy,
            "page_id": "newsletter-form",
            "page_title": "Subscribe to Newsletter",
            "meta_title": "Subscribe to Newsletter",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/form.html", context)

    if request.method != "POST":
        return HttpResponseNotAllowed(["GET", "POST"])

    email_input = request.POST.get("email", "").strip().lower()
    log_newsletter_event(request, "newsletter_subscribe_attempt", email=email_input)

    if request.POST.get("website"):
        log_newsletter_event(
            request, "newsletter_subscribe_failure", email=email_input, result="honeypot"
        )
        message = (
            copy["success"]
            if settings.OPT_IN_MODE == "double"
            else copy["success_no_confirm"]
        )
        context = {
            "message": message,
            "copy": copy,
            "page_id": "newsletter-confirm",
            "page_title": "Subscription Received",
            "meta_title": "Subscription Received",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/confirm.html", context)

    form = NewsletterSubscribeForm(request.POST)
    if not form.is_valid():
        log_newsletter_event(
            request, "newsletter_subscribe_failure", email=email_input, result="validation"
        )
        context = {
            "form": form,
            "copy": copy,
            "page_id": "newsletter-form",
            "page_title": "Subscribe to Newsletter",
            "meta_title": "Subscribe to Newsletter",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/form.html", context)

    email = form.cleaned_data["email"].strip().lower()
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    ip = request.META.get("REMOTE_ADDR", "")

    limits = getattr(
        settings, "NEWSLETTER_RATE_LIMITS", {"ip_per_hour": 10, "email_per_hour": 5}
    )
    ip_key = f"nl:ip:{ip}"
    email_key = f"nl:email:{email_hash}"
    if cache.get(ip_key, 0) >= limits.get("ip_per_hour", 10) or cache.get(
        email_key, 0
    ) >= limits.get("email_per_hour", 5):
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.SERVER_BUSY.value,
        )
        form.add_error(None, copy["server_busy"])
        context = {
            "form": form,
            "copy": copy,
            "page_id": "newsletter-form",
            "page_title": "Subscribe to Newsletter",
            "meta_title": "Subscribe to Newsletter",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/form.html", context)

    cache.set(ip_key, cache.get(ip_key, 0) + 1, 3600)
    cache.set(email_key, cache.get(email_key, 0) + 1, 3600)

    provider = get_provider(
        ip=ip, ua=request.META.get("HTTP_USER_AGENT", ""), source="signup"
    )
    start = time.monotonic()
    try:
        result = provider.subscribe(email)
        duration = (time.monotonic() - start) * 1000
    except TimeoutError:
        duration = (time.monotonic() - start) * 1000
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.SERVER_BUSY.value,
            duration_ms=duration,
        )
        form.add_error(None, copy["server_busy"])
        context = {
            "form": form,
            "copy": copy,
            "page_id": "newsletter-form",
            "page_title": "Subscribe to Newsletter",
            "meta_title": "Subscribe to Newsletter",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/form.html", context)
    except Exception:
        duration = (time.monotonic() - start) * 1000
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.ERROR.value,
            duration_ms=duration,
        )
        form.add_error(None, copy["error"])
        context = {
            "form": form,
            "copy": copy,
            "page_id": "newsletter-form",
            "page_title": "Subscribe to Newsletter",
            "meta_title": "Subscribe to Newsletter",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/form.html", context)

    if result in (Result.SUCCESS, Result.ALREADY, Result.NEEDS_CONFIRM):
        if settings.OPT_IN_MODE == "double" or result == Result.NEEDS_CONFIRM:
            message = copy["success"]
        else:
            message = copy["success_no_confirm"]
        log_newsletter_event(
            request,
            "newsletter_subscribe_success",
            email=email,
            result=result.value,
            duration_ms=duration,
        )
        context = {
            "message": message,
            "copy": copy,
            "page_id": "newsletter-confirm",
            "page_title": "Subscription Received",
            "meta_title": "Subscription Received",
            "meta_robots": "noindex",
        }
        return _render_noindex(request, "newsletter/confirm.html", context)

    if result == Result.SERVER_BUSY:
        form.add_error(None, copy["server_busy"])
    else:
        form.add_error(None, copy["error"])
    log_newsletter_event(
        request,
        "newsletter_subscribe_failure",
        email=email,
        result=result.value,
        duration_ms=duration,
    )
    context = {
        "form": form,
        "copy": copy,
        "page_id": "newsletter-form",
        "page_title": "Subscribe to Newsletter",
        "meta_title": "Subscribe to Newsletter",
        "meta_robots": "noindex",
    }
    return _render_noindex(request, "newsletter/form.html", context)


def newsletter_subscribe(request):
    """Backward compatible alias for newsletter_form."""
    return newsletter_form(request)

