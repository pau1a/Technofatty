import json
from pathlib import Path


def get_signals_content() -> dict:
    """Load signals content spec from JSON."""
    path = Path(__file__).resolve().parent / "content" / "signals.json"
    with path.open() as f:
        return json.load(f)
