from django.conf import settings as app_settings

TEMPLATE_EXPOSED_SETTINGS = getattr(app_settings, 
    'TEMPLATE_EXPOSED_SETTINGS', ['DEBUG', ])


def settings(request):    
    values = {}
    for key in TEMPLATE_EXPOSED_SETTINGS:
        values[key] = getattr(app_settings, key)
    
    return {'settings': values}

   
def full_request_url(request):
    """
    Returns the request's URL in the form 
    http(s)://myhostname.com/my-view/?x=1&y=2
    
    """    
    path = request.get_full_path()
    return {'FULL_REQUEST_URL': request.build_absolute_uri(path)}


def full_request_host(request):
    """
    Returns the request's HTTP host in the form http(s)://myhostname.com
    
    """
    try:
        full_host = ''.join(('http', ('', 's')[request.is_secure()], '://', 
            request.get_host()))
    except KeyError:
        full_host = '' 
    return {'FULL_REQUEST_HOST': full_host}
