# Avoid widows using a template filter
# http://djangosnippets.org/snippets/17/
from __future__ import unicode_literals

from django.template import Library

register = Library()


def widont(value):
    bits = value.rsplit(' ', 1)
    try:
        return bits[0] + "&nbsp;" + bits[1]
    except:
        return value

register.filter(widont)
