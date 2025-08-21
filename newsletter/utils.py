import hashlib
import logging

from django.conf import settings

logger = logging.getLogger(__name__)


def log_newsletter_event(request, event: str, email: str = "", result: str = "", duration_ms: float = 0.0) -> None:
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
