from django import template

from utils.nav import is_active

register = template.Library()


@register.filter(name="nav_active")
def nav_active(request_path: str, link_url: str) -> bool:
    """Return True when ``link_url`` should be marked active for ``request_path``."""
    return is_active(request_path, link_url)
