from __future__ import annotations

from datetime import datetime


def to_iso8601(dt: datetime) -> str:
    """Return ISO-8601 string for a timezone-aware datetime.

    Raises:
        ValueError: If ``dt`` is naive (lacks timezone info).
    """
    if dt.tzinfo is None or dt.tzinfo.utcoffset(dt) is None:
        raise ValueError("datetime must be timezone-aware")
    return dt.isoformat()
