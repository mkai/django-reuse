from django.http import HttpResponse
from django.conf import settings


class HTTPBasicAuthMiddleware(object):
    """
    A very basic Basic Auth middleware that uses a username/password defined in your settings.py as BASICAUTH_USERNAME and BASICAUTH_PASSWORD. Does not use Django auth. Handy for quickly securing an entire site during development, for example.

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
