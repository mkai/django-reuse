import os
import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.hashcompat import md5_constructor
from django.core.cache.backends.base import (MEMCACHE_MAX_KEY_LENGTH,
                                             default_key_func)


def file_from_url(url):
    """Returns a file object from the data downloaded from the given URL."""
    try:
        request = urllib2.urlopen(url)

        temp_file = NamedTemporaryFile()
        temp_file.write(request.read())
        temp_file.flush()

        file_name = urllib2.unquote(os.path.basename(request.geturl()))
        file_instance = File(temp_file)

        return file_name, file_instance
    except:
        return None


def safe_cache_key(key, key_prefix, version):
    """Hashes cache keys that are longer than MEMCACHE_MAX_KEY_LENGTH chars."""
    result = default_key_func(key, key_prefix, version)
    if len(result) > MEMCACHE_MAX_KEY_LENGTH:
        result = md5_constructor(result).hexdigest()
    return result
