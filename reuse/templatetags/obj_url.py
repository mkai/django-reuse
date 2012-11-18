from django import template
from django.core.urlresolvers import reverse

register = template.Library()


@register.assignment_tag
def obj_url(obj, url_format):
    """
    Returns a reversed URL from a given object's attribute value and other URL
    arguments given in a format string.

    This makes it possible to reuse template snippets, e. g. a list of tags in
    which you would like to make configurable where each tag links to, and
    the link is dependent on an object's attribute, e. g. its slug or pk. You
    would then pass an argument like "link_format" to the template snippet and
    use this template tag and the format string to get a reversed URL.

    In the format string, each value surround by < > braces will be resolved
    from the given object using getattr.

    Format: <url name>/<<object attribute name>>/<another arg>/<another>[/]
    Example format: book_list/<slug>/

    Usage:
        {% obj_url tag "book_list/<slug>/" %}

    """
    # separate url name and arguments, remove empty strings
    pieces = [p for p in url_format.split('/') if p.strip()]
    url_name, args = pieces.pop(0), pieces

    # get dynamic args ('<attr>') from the object
    resolve_attrs = (lambda a: a if not a.startswith('<')
                               else getattr(obj, a.strip('<>')))
    args = map(resolve_attrs, args)
    return reverse(url_name, args=args)
