from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage

CACHE_PARAM = getattr(settings, 'STATICFILES_CACHE_PARAM', '?0')


class ParameterCachedStaticFilesStorage(StaticFilesStorage):
    """
    
    """
    def url(self, name):
        url = super(ParameterCachedStaticFilesStorage, self).url(name)
        
        return url + CACHE_PARAM
