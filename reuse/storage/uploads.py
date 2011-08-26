from django.conf import settings
from storages.backends.sftpstorage import SFTPStorage

class HTTPSFTPStorage(SFTPStorage):
    base_url = settings.MEDIA_URL
    
    def url(self, name):
        return self.base_url + name
