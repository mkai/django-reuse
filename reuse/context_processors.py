def settings(request):
    from django.conf import settings
    
    values = {}
    for setting in settings.TEMPLATE_EXPOSED_SETTINGS:
        values[setting] = getattr(settings, setting)
    
    return { 'settings': values }
   
def full_request_url(request):
    """
    Returns the request's URL in the form http(s)://myhostname.com/my-view/?x=1&y=2
    
    """    
    return { 'FULL_REQUEST_URL': request.build_absolute_uri(request.get_full_path()) }


def full_request_host(request):
    """
    Returns the request's HTTP host in the form http(s)://myhostname.com
    
    """
    try:
        full_host = ''.join(('http', ('', 's')[request.is_secure()], '://', request.get_host()))
    except KeyError:
       full_host = '' 

    return { 'FULL_REQUEST_HOST': full_host }
