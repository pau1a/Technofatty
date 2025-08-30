import hashlib
import logging
from typing import Any, Dict
from urllib.parse import urlencode

from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags

logger = logging.getLogger(__name__)


def log_newsletter_event(
    request, event: str, email: str = "", result: str = "", duration_ms: float = 0.0
) -> None:
    ip = request.META.get("REMOTE_ADDR", "")
    ua = request.META.get("HTTP_USER_AGENT", "")
    email_hash = hashlib.sha256(email.encode()).hexdigest() if email else ""
    logger.info(
        {
            "event": event,
            "email_hash": email_hash,
            "ip": ip,
            "ua": ua,
            "provider": getattr(settings, "NEWSLETTER_PROVIDER", ""),
            "result": result,
            "opt_in_mode": getattr(settings, "OPT_IN_MODE", ""),
            "duration_ms": int(duration_ms),
        }
    )


def extract_block_context(obj: Any) -> Dict[str, str]:
    """Return title, excerpt and hero image URL for newsletter blocks.

    The function accepts any object with ``title`` and optionally ``excerpt`` or
    ``summary``/``blurb`` attributes. Hero images are pulled from ``image`` or
    ``og_image_url`` if present. ``get_absolute_url`` is used when available so
    the block can link back to the source page.
    """

    title = getattr(obj, "title", "")

    excerpt = (
        getattr(obj, "excerpt", "")
        or getattr(obj, "summary", "")
        or getattr(obj, "blurb", "")
    )

    image_url = ""
    image = getattr(obj, "image", None)
    if image:
        image_url = getattr(image, "url", image)
    else:
        image_url = getattr(obj, "og_image_url", "")

    alt = getattr(obj, "image_alt", "") or title

    url = getattr(obj, "canonical_url", "")
    if not url and hasattr(obj, "get_absolute_url"):
        try:
            url = obj.get_absolute_url()
        except Exception:  # pragma: no cover - defensive, should not happen
            url = ""

    def _abs(u: str) -> str:
        base = getattr(settings, "SITE_BASE_URL", "").rstrip("/")
        if base and u and u.startswith("/"):
            return f"{base}{u}"
        return u

    def with_utm(u: str) -> str:
        params = getattr(
            settings,
            "NEWSLETTER_UTM",
            {"source": "newsletter", "medium": "email", "campaign": "weekly"},
        )
        sep = "&" if "?" in u else "?"
        return f"{u}{sep}{urlencode({'utm_source': params['source'], 'utm_medium': params['medium'], 'utm_campaign': params['campaign']})}"

    def truncate_words(s: str, limit: int = 200) -> str:
        s = s.strip()
        if len(s) <= limit:
            return s
        cut = s.rfind(" ", 0, limit)
        return (s[:cut] if cut > 0 else s[:limit]).rstrip() + "…"

    url = _abs(url)
    image_url = _abs(image_url)
    if url:
        url = with_utm(url)

    text = strip_tags(excerpt or "")
    excerpt = truncate_words(text)

    return {
        "title": title,
        "excerpt": excerpt,
        "image_url": image_url,
        "url": url,
        "alt": alt,
    }


def render_block(obj: Any) -> str:
    """Render a newsletter HTML block for the given object."""

    context = extract_block_context(obj)
    return render_to_string("newsletter/block.html", context)
