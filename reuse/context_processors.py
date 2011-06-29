def settings(request):
    from django.conf import settings
    
    values = {}
    for setting in settings.TEMPLATE_EXPOSED_SETTINGS:
        values[setting] = getattr(settings, setting)
    
    return { 'settings': values }
   
def full_request_url(request):
    """
    Returns the request's URL in the form http(s)://myhostname.com/my-view/
    """
    try:
        full_path = ''.join(('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST'], request.path))
    except KeyError:
        full_path = ''
    
    return { 'FULL_REQUEST_URL': full_path }


def full_request_host(request):
    """
    Returns the request's HTTP host in the form http(s)://myhostname.com
    """
    try:
        full_host = ''.join(('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST']))
    except KeyError:
       full_host = '' 

    return { 'FULL_REQUEST_HOST': full_host }
    