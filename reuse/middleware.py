import re
from django.contrib.sites.models import Site
from django.http import HttpResponse, HttpResponsePermanentRedirect
from django.conf import settings


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
    def unauthed(self):
        response = HttpResponse("""<html><title>Auth required</title><body>
                                <h1>Authorization Required</h1></body></html>""", mimetype="text/html")
        response['WWW-Authenticate'] = 'Basic realm="Development"'
        response.status_code = 401
        return response
    
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
            if username == settings.BASIC_AUTH_USERNAME and password == settings.BASIC_AUTH_PASSWORD:
                return None            
            return self.unauthed()


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
        if settings.DEBUG == True:
            return None

        domain = getattr(settings, 'SITE_DOMAIN', None)
        if not domain:
            domain = Site.objects.get_current().domain

        if domain in request.get_host():
            return None
        return HttpResponsePermanentRedirect('%s://%s%s' % (
            request.is_secure() and 'https' or 'http',
            domain,
            request.get_full_path(),
        ))


class StripWhitespaceMiddleware(object):
    """
    Strips leading and trailing whitespace from an HTML response's content.

    From: https://bitbucket.org/zalew/django-annoying

    """
    def __init__(self):
        self.whitespace = re.compile('\s*\n')

    def process_response(self, request, response):
        if 'text/html' in response['Content-Type'].lower():
            new_content = self.whitespace.sub('\n', response.content)
            response.content = new_content
        return response 
