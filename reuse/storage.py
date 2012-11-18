from django.conf import settings
from django.contrib.staticfiles.storage import StaticFilesStorage
from storages.backends.sftpstorage import SFTPStorage


CACHE_PARAM = getattr(settings, 'STATICFILES_CACHE_PARAM', '?v=1')


class ParameterCachedStaticFilesStorage(StaticFilesStorage):
    """
    A static files storage backend that appends a static parameter to the
    request file's URL.

    Note that this is a far from ideal solution because the parameter is the
    same for all referenced files. If it changes, all files will be removed
    from the browser cache and will be redownloaded.

    """
    def url(self, name):
        url = super(ParameterCachedStaticFilesStorage, self).url(name)
        return url + CACHE_PARAM


class HTTPSFTPStorage(SFTPStorage):
    """
    A storage backend that uploads files to an FTP server and references them
    under the URL accessible by an HTTP server.

    The HTTP URL must be given as SFTP_STORAGE_HTTP_ROOT in settings.

    """
    base_url = settings.SFTP_STORAGE_HTTP_ROOT

    def url(self, name):
        return self.base_url + name
