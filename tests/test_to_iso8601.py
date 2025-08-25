import pathlib
import sys
from datetime import datetime, timezone

import pytest

sys.path.append(str(pathlib.Path(__file__).resolve().parents[1]))

from utils.dates import to_iso8601
from utils.partials import article_partial, case_study_partial


def test_to_iso8601_formats_aware_datetime():
    dt = datetime(2024, 5, 1, 10, 0, tzinfo=timezone.utc)
    assert to_iso8601(dt) == "2024-05-01T10:00:00+00:00"


def test_to_iso8601_raises_for_naive_datetime():
    dt = datetime(2024, 5, 1, 10, 0)
    with pytest.raises(ValueError):
        to_iso8601(dt)


def test_article_partial_uses_iso_format():
    pub = datetime(2024, 5, 1, 10, 0, tzinfo=timezone.utc)
    mod = datetime(2024, 5, 2, 12, 0, tzinfo=timezone.utc)
    data = article_partial(
        "https://example.com/blog/my-post",
        pub,
        modified=mod,
        author={"@type": "Person", "name": "Alice"},
    )
    assert data["datePublished"] == "2024-05-01T10:00:00+00:00"
    assert data["dateModified"] == "2024-05-02T12:00:00+00:00"


def test_case_study_partial_requires_aware_datetime():
    pub = datetime(2024, 3, 15, 9, 30, tzinfo=timezone.utc)
    publisher = {"@type": "Organization", "name": "Example Co", "url": "https://example.com"}
    data = case_study_partial(
        "https://example.com/case-studies/acme",
        pub,
        publisher,
    )
    assert data["datePublished"] == "2024-03-15T09:30:00+00:00"
    with pytest.raises(ValueError):
        case_study_partial(
            "https://example.com/case-studies/acme",
            datetime(2024, 3, 15, 9, 30),
            publisher,
        )
