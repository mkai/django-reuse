from __future__ import unicode_literals

from django import template

register = template.Library()


@register.assignment_tag
def assign(value):
    return value
