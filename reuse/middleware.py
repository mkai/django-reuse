from __future__ import unicode_literals

import re
from django.conf import settings
from django.http import (HttpResponse, HttpResponseRedirect,
                         HttpResponsePermanentRedirect)
from django.utils.html import strip_spaces_between_tags
from django.utils.translation import ugettext_lazy as _
from django.contrib.sites.models import get_current_site
from django.contrib.redirects.models import Redirect


class SSLRedirectMiddleware(object):
    """Redirects all non-HTTPS requests to their equivalent HTTPS URL."""
    def __init__(self, *args, **kwargs):
        self.enabled = getattr(settings, 'SSL_REDIRECT_ENABLED', False)
        self.redirect_port = getattr(settings, 'SSL_REDIRECT_PORT', None)
        self.redirect_cls = HttpResponsePermanentRedirect
        if not getattr(settings, 'SSL_REDIRECT_PERMANENT', True):
            self.redirect_cls = HttpResponseRedirect

    def process_request(self, request):
        # if disabled or already HTTPS, do nothing
        if not self.enabled or request.is_secure():
            return None
        # replace protocol
        url = request.build_absolute_uri()
        secure_url = url.replace('http://', 'https://', 1)
        # apply custom redirect port if set
        # seems like this should be easier...
        if self.redirect_port and self.redirect_port not in (80, 443):
            current_port = request.META['SERVER_PORT']
            if current_port == '80' and not ':80' in secure_url:
                secure_url = secure_url + ':{}'.format(self.redirect_port)
            else:
                secure_url = secure_url.replace(':{}'.format(current_port),
                                                ':{}'.format(self.redirect_port))
        return self.redirect_cls(secure_url)


class HTTPBasicAuthMiddleware(object):
    """
    A very basic Basic Auth middleware that uses a username/password defined
    in your settings.py as BASIC_AUTH_USERNAME and BASIC_AUTH_PASSWORD.
    Does not use Django auth. Handy for quickly securing an entire site during
    development, for example.

    In settings.py:

    BASIC_AUTH_USERNAME = 'user'
    BASIC_AUTH_PASSWORD = 'pass'

    MIDDLEWARE_CLASSES = (
        'app.module.BasicAuthMiddleware',
        #all other middleware
    )

    From: joshsharp http://djangosnippets.org/snippets/2468/

    """
    def process_request(self, request):
        if not 'HTTP_AUTHORIZATION' in request.META:
            return self.unauthed()
        else:
            authentication = request.META['HTTP_AUTHORIZATION']
            (authmeth, auth) = authentication.split(' ', 1)
            if 'basic' != authmeth.lower():
                return self.unauthed()
            auth = auth.strip().decode('base64')
            username, password = auth.split(':', 1)
            if (username == settings.BASIC_AUTH_USERNAME and
                    password == settings.BASIC_AUTH_PASSWORD):
                return None
            return self.unauthed()

    def unauthed(self):
        html = "<html><title>{msg}</title><body><h1>{msg}</h1></body></html>"
        response = HttpResponse(html.format(msg=_("Authorization required.")),
                                content_type="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response


class DefaultSiteRedirectMiddleware(object):
    """
    Redirects all requests to a common domain, e. g.:
        example.com -> www.example.com
        example.net -> www.example.com
        www.example.de -> www.example.com

    The common domain can be specified in a Django setting named SITE_DOMAIN.
    If SITE_DOMAIN is not set, the domain of the default Site (as in
    django.contrib.sites) is used.

    Doesn't do anything during development, i. e. if DEBUG is set to True.

    Adapted from: jezdez http://djangosnippets.org/snippets/989/

    """
    def process_request(self, request):
        if settings.DEBUG is True:
            return None
        domain = getattr(settings, 'SITE_DOMAIN', None)
        if not domain:
            domain = get_current_site(request).domain
        if domain in request.get_host():
            return None
        return HttpResponsePermanentRedirect('{}://{}{}'.format(
            request.is_secure() and 'https' or 'http',
            domain,
            request.get_full_path(),
        ))


EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/'))]
if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        assert hasattr(request, 'user'), "The Login Required middleware\
 requires authentication middleware to be installed. Edit your\
 MIDDLEWARE_CLASSES setting to insert\
 'django.contrib.auth.middlware.AuthenticationMiddleware'. If that doesn't\
 work, ensure your TEMPLATE_CONTEXT_PROCESSORS setting includes\
 'django.core.context_processors.auth'."
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)


class StripWhitespaceMiddleware(object):
    """
    Strips whitespace from an HTML response's content.

    From: http://justcramer.com/2008/12/01/spaceless-html-in-django/

    """
    def process_response(self, request, response):
        if 'text/html' in response.get('Content-Type', '').lower():
            response.content = strip_spaces_between_tags(response.content.strip())
        return response


class MalformedQueryStringMiddleware(object):
    """
    Detects a malformed query string and redirects to a sanitized version of
    the requested URL.

    Put it before CommonMiddleware in MIDDLEWARE_CLASSES.

    Example: redirect http://site.com/&a=x&b=y to http://site.com/?a=x&b=y

    """
    def process_request(self, request):
        if '&' in request.path:  # '&' left over from a malformed query string
            url = request.path.replace('&', '?', 1)
            if request.META.get('QUERY_STRING', ''):
                # append regular query string
                url += '&' + request.META['QUERY_STRING']
            return HttpResponsePermanentRedirect(url)


class RegExRedirectFallbackMiddleware(object):
    """
    Simple middleware to complement the built in redirect middleware app.
    Add this after the contrib.redirect middleware - this will be fired if
    a 404 is triggered and the contrib.redirect fails to find a suitable
    redirect.

    Useful if you want to add the redirects into the DB - and/or don't have
    access to the .htaccess script or whatever HTTP server based redirect
    machinery your site runs off.

    From: http://djangosnippets.org/snippets/2784/

    """
    def process_response(self, request, response):
        if response.status_code != 404:
            return response  # only check 404 responses.
        path = request.get_full_path()
        redirects = Redirect.objects.filter(site__id__exact=settings.SITE_ID)
        for r in redirects:
            try:
                old_path = re.compile(r.old_path, re.IGNORECASE)
            except re.error:
                # old_path does not compile into regex,
                # ignore it and move on to the next one
                continue
            if re.match(r.old_path, path):
                new_path = r.new_path.replace('$', '\\')
                replaced_path = re.sub(old_path, new_path, path)
                return HttpResponsePermanentRedirect(replaced_path)
        return response
