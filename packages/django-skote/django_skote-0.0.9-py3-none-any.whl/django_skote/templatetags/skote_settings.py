from django import template
from django.conf import settings

register = template.Library()


# settings value
@register.simple_tag
def skote_settings(name):
    return getattr(settings, name, "")
