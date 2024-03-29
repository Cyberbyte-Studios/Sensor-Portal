from django import template
from django.conf import settings
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def error_reporting():
    html = 'console.warn(\'DEBUG = True\')'
    if not settings.DEBUG:
        from raven.contrib.django.models import client
        dsn = client.get_public_dsn()
        if dsn:
            html = 'Raven.config(\'{}\').install();'.format(dsn)

    return mark_safe(html)
