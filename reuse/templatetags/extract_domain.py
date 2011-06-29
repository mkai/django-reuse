from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter
@stringfilter
def domain_name(url, strip_extra = ''):
    return url.replace('http://', '').replace('https://', '').partition('/')[0].replace(strip_extra, '')

