import json
from pathlib import Path


def get_support_content() -> dict:
    """Load support content spec from JSON."""
    path = Path(__file__).resolve().parent / "content" / "support.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)
