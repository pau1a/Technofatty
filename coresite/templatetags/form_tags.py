from django import template

register = template.Library()

@register.simple_tag
def add_attrs(field, **attrs):
    """Render a form field with additional HTML attributes."""
    return field.as_widget(attrs=attrs)
