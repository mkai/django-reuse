from __future__ import unicode_literals

from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@register.filter
@stringfilter
def domain_name(url, strip_extra=''):
    domain = url.replace('http://', '')
    domain = domain.replace('https://', '')
    domain = domain.partition('/')[0]
    if strip_extra:
        domain = domain.replace(strip_extra, '')
    return domain
