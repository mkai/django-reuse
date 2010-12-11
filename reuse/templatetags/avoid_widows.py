# Avoid widows using a template filter
# http://djangosnippets.org/snippets/17/

from django.template import Library, Node

register = Library()

def widont(value):
    bits = value.rsplit(' ', 1)
    try:
        widowless = bits[0] + "&nbsp;" + bits[1]
        return widowless
    except:
        return value

register.filter(widont)
