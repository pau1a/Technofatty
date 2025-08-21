import hashlib
import time

from django.conf import settings
from django.contrib import messages
from django.core.cache import cache
from django.http import HttpResponseNotAllowed
from django.shortcuts import redirect
from django.urls import reverse

from .copy import get_copy
from .forms import NewsletterSubscribeForm
from .providers import Result, get_provider
from .utils import log_newsletter_event


def newsletter_subscribe(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    copy = get_copy()
    email_input = request.POST.get("email", "").strip().lower()
    log_newsletter_event(request, "newsletter_subscribe_attempt", email=email_input)

    if request.POST.get("website"):
        messages.success(
            request,
            copy["success_no_confirm"] if settings.OPT_IN_MODE == "single" else copy["success"],
        )
        log_newsletter_event(
            request, "newsletter_subscribe_failure", email=email_input, result="honeypot"
        )
        return redirect(reverse("home") + "#signup")

    form = NewsletterSubscribeForm(request.POST)
    if not form.is_valid():
        if "email" in form.errors:
            messages.error(request, form.errors["email"][0])
            log_newsletter_event(
                request, "newsletter_subscribe_failure", email=email_input, result="validation"
            )
        else:
            messages.success(
                request,
                copy["success_no_confirm"] if settings.OPT_IN_MODE == "single" else copy["success"],
            )
            log_newsletter_event(
                request, "newsletter_subscribe_failure", email=email_input, result="honeypot"
            )
        return redirect(reverse("home") + "#signup")

    email = form.cleaned_data["email"].strip().lower()
    email_hash = hashlib.sha256(email.encode()).hexdigest()
    ip = request.META.get("REMOTE_ADDR", "")

    limits = getattr(
        settings,
        "NEWSLETTER_RATE_LIMITS",
        {"ip_per_hour": 10, "email_per_hour": 5},
    )
    ip_key = f"nl:ip:{ip}"
    email_key = f"nl:email:{email_hash}"
    if cache.get(ip_key, 0) >= limits.get("ip_per_hour", 10) or cache.get(
        email_key, 0
    ) >= limits.get("email_per_hour", 5):
        messages.error(request, copy["server_busy"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.SERVER_BUSY.value,
        )
        return redirect(reverse("home") + "#signup")

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
        messages.error(request, copy["server_busy"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.SERVER_BUSY.value,
            duration_ms=duration,
        )
        return redirect(reverse("home") + "#signup")
    except Exception:
        duration = (time.monotonic() - start) * 1000
        messages.error(request, copy["error"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=Result.ERROR.value,
            duration_ms=duration,
        )
        return redirect(reverse("home") + "#signup")

    if result in (Result.SUCCESS, Result.ALREADY, Result.NEEDS_CONFIRM):
        if settings.OPT_IN_MODE == "double" or result == Result.NEEDS_CONFIRM:
            messages.success(request, copy["success"])
        else:
            messages.success(request, copy["success_no_confirm"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_success",
            email=email,
            result=result.value,
            duration_ms=duration,
        )
    elif result == Result.SERVER_BUSY:
        messages.error(request, copy["server_busy"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=result.value,
            duration_ms=duration,
        )
    else:
        messages.error(request, copy["error"])
        log_newsletter_event(
            request,
            "newsletter_subscribe_failure",
            email=email,
            result=result.value,
            duration_ms=duration,
        )

    return redirect(reverse("home") + "#signup")
