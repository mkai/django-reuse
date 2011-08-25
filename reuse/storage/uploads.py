from django.conf import settings
from storages.backends.sftpstorage import SFTPStorage

class HTTPSFTPStorage(SFTPStorage):
    """
    
    """
    def url(self, name):
        return settings.MEDIA_URL + name
