from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode, urljoin

from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag(takes_context=True)
def canonical_url(context, url=None):
    request = context.get("request")
    base = getattr(settings, "SITE_BASE_URL", None) or (
        f"https://{getattr(settings, 'SITE_CANONICAL_HOST', '')}"
        if getattr(settings, "SITE_CANONICAL_HOST", "")
        else None
    )

    if url:
        parsed = urlparse(url)
        if not parsed.scheme:
            if request:
                url = request.build_absolute_uri(url)
            elif base:
                url = urljoin(base, url)
            else:
                return ""
    else:
        if request:
            url = request.build_absolute_uri()
        elif base:
            url = base
        else:
            return ""

    parsed = urlparse(url)
    query = dict(parse_qsl(parsed.query, keep_blank_values=True))
    if query.get("page") == "1":
        del query["page"]
    query_string = urlencode(query, doseq=True)
    new_parsed = parsed._replace(query=query_string)
    cleaned = urlunparse(new_parsed)
    if cleaned.endswith("?"):
        cleaned = cleaned[:-1]
    return cleaned
