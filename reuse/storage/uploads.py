from django.conf import settings
from storages.backends.sftpstorage import SFTPStorage


class HTTPSFTPStorage(SFTPStorage):
    base_url = settings.SFTP_STORAGE_HTTP_ROOT
        
    def url(self, name):
        return self.base_url + name
