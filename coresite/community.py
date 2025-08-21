import json
from pathlib import Path


def get_community_content() -> dict:
    """Load community content spec from JSON."""
    path = Path(__file__).resolve().parent / "content" / "community.json"
    with path.open(encoding="utf-8") as f:
        return json.load(f)
