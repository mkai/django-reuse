# http://gnuvince.wordpress.com/2007/09/14/a-django-template-tag-for-the-current-active-page/
# http://gnuvince.wordpress.com/2007/09/14/a-django-template-tag-for-the-current-active-page/#comment-2023

from django.template import Library
register = Library()

@register.simple_tag
def active_url(request, pattern, return_value):
    import re
    if re.search(pattern, request.path):
        return return_value
    return ''

@register.simple_tag
def active_view(request, url, return_value):
    from django.core.urlresolvers import reverse
    if reverse(url) == request.path:
        return return_value
    return ''
