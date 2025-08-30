from datetime import datetime
from typing import List, Tuple

# Simple in-memory store of gaps and persisted log for future triage
GAPS: List[Tuple[str, str, datetime]] = []


def log_gap(kind: str, location: str) -> None:
    """Record a missing content gap for later review.

    Args:
        kind: Type of content that was missing (e.g. "knowledge" or "tools").
        location: Where the gap was encountered.
    """
    entry = (kind, location, datetime.utcnow())
    GAPS.append(entry)
    try:
        with open(__file__.rsplit("/", 1)[0] + "/backlog.log", "a", encoding="utf-8") as fh:
            fh.write(f"{entry[2].isoformat()}|{kind}|{location}\n")
    except OSError:
        # If the log file can't be written, fail silently; the in-memory
        # record is still available for inspection in tests.
        pass
