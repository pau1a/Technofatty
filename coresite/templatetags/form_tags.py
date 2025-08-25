from django import template

register = template.Library()

@register.simple_tag
def add_attrs(field, **attrs):
    """Render a form field with additional HTML attributes.

    Hyphenated attribute names can be passed using underscores in the
    template, e.g. ``aria_describedby``.
    """
    normalized = {key.replace("_", "-"): value for key, value in attrs.items()}
    return field.as_widget(attrs=normalized)
