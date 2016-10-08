from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def error_reporting(scheme=None):
    if not settings.DEBUG:
        from raven.contrib.django.models import client
        dsn = client.get_public_dsn(scheme)
        if dsn:
            return 'Raven.config(' + dsn + ').install()'
    return 'console.warn(\'DEBUG = True\')'
