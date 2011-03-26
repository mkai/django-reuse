# adapted from source: http://code.djangoproject.com/ticket/5025
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()

@register.filter(name='truncatechars')
@stringfilter
def truncatechars(value, arg):
    """
    Truncates a string after a certain number of characters.
    
    Argument: Number of characters to truncate after.
    """
    from reuse.utils.truncate_chars import truncate_chars
    try:
        length = int(arg)
    except ValueError: # Invalid literal for int().
        return value # Fail silently.
    return truncate_chars(value, length)
truncatechars.is_safe = True
