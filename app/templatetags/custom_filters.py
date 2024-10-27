import base64
from django import template

register = template.Library()

@register.filter
def b64encode(value):
    return base64.b64encode(value).decode('utf-8') if value else ''

@register.filter
def get_attribute(obj, attr_name):
    """Return the attribute of the object with the given name."""
    return getattr(obj, attr_name, None)

@register.filter
def times(value):
    return range(value)