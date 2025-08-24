from urllib.parse import urlparse, urlunparse, parse_qsl, urlencode

from django import template


register = template.Library()


@register.simple_tag(takes_context=True)
def canonical_url(context, url=None):
    request = context.get("request")
    if url:
        parsed = urlparse(url)
        if not parsed.scheme:
            url = request.build_absolute_uri(url)
    else:
        url = request.build_absolute_uri()
        parsed = urlparse(url)
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
