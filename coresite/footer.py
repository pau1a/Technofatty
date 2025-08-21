"""Footer content loader."""

import json
from datetime import datetime
from functools import lru_cache
from pathlib import Path
from copy import deepcopy


@lru_cache(maxsize=1)
def _load_footer_json() -> dict:
    """Load footer JSON from disk once per process."""
    path = Path(__file__).resolve().parent / "content" / "footer.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def get_footer_content() -> dict:
    """Return footer content with current year injected.

    The JSON is cached in-process to avoid disk I/O on each request. Each call
    injects the current year so the rendered copyright stays fresh.
    """

    content = deepcopy(_load_footer_json())

    year = str(datetime.now().year)
    meta = content.get("meta", {})
    copyright = meta.get("copyright")
    if copyright:
        meta["copyright"] = copyright.replace("{{year}}", year)

    return content
