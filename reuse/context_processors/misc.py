def app_name(request):
    from django.conf import settings
    
    return { 'APP_NAME': settings.APP_NAME }


def google_analytics_id(request):
    from django.conf import settings
    
    return { 'GOOGLE_ANALYTICS_ID': settings.GOOGLE_ANALYTICS_ID }


def facebook_api_key(request):
    from django.conf import settings

    return { 'FACEBOOK_API_KEY': settings.FACEBOOK_API_KEY }


def facebook_app_id(request):
    from django.conf import settings
    
    return { 'FACEBOOK_APP_ID': settings.FACEBOOK_APP_ID }    


def cache_buster_key(request):
    from django.conf import settings

    return { 'CACHE_BUSTER_KEY': settings.CACHE_BUSTER_KEY }
        

def debug(request):
    from django.conf import settings
    
    debug_var = 'false'
    if settings.DEBUG:
        debug_var = 'true'
    
    return { 'DEBUG': debug_var }


def full_request_url(request):
    """
    Returns the request's URL in the form http(s)://myhostname.com/my-view/
    """
    full_path = ''.join(('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST'], request.path))
    
    return { 'FULL_REQUEST_URL': full_path }


def full_request_host(request):
    """
    Returns the request's HTTP host in the form http(s)://myhostname.com
    """
    full_host = ''.join(('http', ('', 's')[request.is_secure()], '://', request.META['HTTP_HOST']))

    return { 'FULL_REQUEST_HOST': full_host }
