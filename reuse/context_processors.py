from __future__ import unicode_literals

from django.conf import settings as app_settings
from .utils import get_request_host, get_request_url


TEMPLATE_EXPOSED_SETTINGS = getattr(app_settings, 'TEMPLATE_EXPOSED_SETTINGS',
                                    ['DEBUG', ])


def settings(request):
    values = {}
    for key in TEMPLATE_EXPOSED_SETTINGS:
        values[key] = getattr(app_settings, key)
    return {'settings': values}


def request_url(request):
    """Returns a request's URL, e. g. http(s)://example.com/path/?x=1&y=2"""
    return {'REQUEST_URL': get_request_url(request)}


def request_host(request):
    """Returns the request host + protocol, e. g. http(s)://example.com"""
    return {'REQUEST_HOST': get_request_host(request)}
