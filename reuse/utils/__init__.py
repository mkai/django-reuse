import os
import requests
import urlparse
from datetime import datetime
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.shortcuts import _get_queryset
from django.utils import timezone
from django.utils.http import urlunquote

# timezone-aware 0-timestamp
TIMEZONE_EPOCH = timezone.make_aware(datetime(1970, 1, 1), timezone.utc)


def file_from_url(url):
    """Returns a file object from the data downloaded from the given URL."""
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 204:  # No content
            return None, None, None
        path = urlparse.urlsplit(response.url).path
        name = urlunquote(os.path.basename(path))
        ctype = response.headers['content-type']

        # create temp file with the downloaded data
        temp_file = NamedTemporaryFile()
        temp_file.write(response.content)
        temp_file.flush()
        fp = File(temp_file)
        fp.seek(0)
    except Exception, e:
        raise IOError(u'Couldn\'t get file from %s: %r' % (url, e))
    return name, fp, ctype


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.

    From: django-annoying

    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None
