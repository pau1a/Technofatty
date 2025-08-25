from __future__ import annotations

from datetime import datetime

from .dates import to_iso8601


def article_partial(
    url: str,
    published: datetime,
    *,
    modified: datetime | None = None,
    author: dict | None = None,
) -> dict:
    """Return JSON-LD data for an article.

    Parameters
    ----------
    url:
        Canonical URL of the article.
    published:
        Publication datetime (timezone-aware).
    modified:
        Last modification datetime. Defaults to ``published``.
    author:
        Optional author dictionary to include.
    """
    data: dict = {
        "@context": "https://schema.org",
        "@type": "Article",
        "url": url,
        "datePublished": to_iso8601(published),
        "dateModified": to_iso8601(modified or published),
    }
    if author:
        data["author"] = author
    return data


def case_study_partial(url: str, published: datetime, publisher: dict) -> dict:
    """Return JSON-LD data for a case study article."""
    return {
        "@context": "https://schema.org",
        "@type": "Article",
        "url": url,
        "datePublished": to_iso8601(published),
        "publisher": publisher,
    }
