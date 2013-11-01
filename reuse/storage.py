from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.staticfiles.storage import StaticFilesStorage


class ParameterCachedStaticFilesStorage(StaticFilesStorage):
    """
    A static files storage backend that appends a static parameter to the
    request file's URL.

    Note that this is a far from ideal solution because the parameter is the
    same for all referenced files. If it changes, all files will be removed
    from the browser cache and will be redownloaded.

    """
    cache_param = getattr(settings, 'STATICFILES_CACHE_PARAM', '?v=1')

    def url(self, name):
        url = super(ParameterCachedStaticFilesStorage, self).url(name)
        return url + self.cache_param


class OverwritingStorageMixin(object):
    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        if self.exists(name):
            self.delete(name)
        return super(OverwritingStorageMixin, self)._save(name, content)


class OverwritingFileSystemStorage(OverwritingStorageMixin, FileSystemStorage):
    """
    A FileSystemStorage that deletes an existing file of the same name
    before saving.

    """
    pass


class KeepExistingStorageMixin(object):
    def get_available_name(self, name):
        return name

    def _save(self, name, content):
        if self.exists(name):
            return name  # do nothing if file exists
        return super(KeepExistingStorageMixin, self)._save(name, content)


class KeepExistingFileSystemStorage(KeepExistingStorageMixin, FileSystemStorage):
    """
    A FileSystemStorage that does nothing if the file to save already
    exists. Useful for deduplicating files.

    """
    pass
