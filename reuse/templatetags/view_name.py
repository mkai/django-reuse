"""
Template tag to resolve an URL to a view name or view function.

Useful in navigation menu templates.

Author: Fahrzin Hemmati
From: http://pastebin.com/7KfALc0j
Originally from: http://djangosnippets.org/snippets/1378/

Usage:
    {% load view_name %}
    {% get_view_name request.path as view_name %}

"""
from django.core.urlresolvers import RegexURLPattern, Resolver404, get_resolver
from django.template import Library

register = Library()


def _pattern_resolve_to_name(self, path):
    match = self.regex.search(path)
    if match:
        name = ""
        if self.name:
            name = self.name
        elif hasattr(self, '_callback_str'):
            name = self._callback_str
        else:
            name = "%s.%s" % (self.callback.__module__, self.callback.func_name)
        return name


def _resolver_resolve_to_name(self, path):
    tried = []
    match = self.regex.search(path)
    if match:
        new_path = path[match.end():]
        for pattern in self.url_patterns:
            if not isinstance(pattern, RegexURLPattern):
                # ignore RegexURLResolver instances matched by an URL like ''
                # (e. g. when an include() is used in the URLconf).
                continue
            try:
                name = _pattern_resolve_to_name(pattern, new_path)
            except Resolver404, e:
                tried.extend([(pattern.regex.pattern + '   ' + t) for t in e.args[0]['tried']])
            else:
                if name:
                    return name
                tried.append(pattern.regex.pattern)
        raise Resolver404, {'tried': tried, 'path': new_path}


@register.assignment_tag(name='get_view_name')
def resolve_to_name(path, urlconf=None):
    r = get_resolver(urlconf)
    if isinstance(r, RegexURLPattern):
        return _pattern_resolve_to_name(r, path)
    else:
        try:
            return _resolver_resolve_to_name(r, path)
        except Resolver404:
            return None
