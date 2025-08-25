import hashlib
import logging
from typing import Any, Dict

logger = logging.getLogger(__name__)


def contact_event(event_type: str, meta: Dict[str, Any]) -> None:
    """Log a contact event and optionally persist it."""
    meta = dict(meta)
    ip = meta.pop("ip", "")
    ip_hash = hashlib.sha256(ip.encode()).hexdigest() if ip else ""
    logger.info({"event": event_type, "meta": meta, "ip_hash": ip_hash})
    try:
        from coresite.models import ContactEvent

        ContactEvent.objects.create(event_type=event_type, meta=meta, ip_hash=ip_hash)
    except Exception:
        pass
