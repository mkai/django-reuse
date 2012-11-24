from django.core.cache.backends.base import (MEMCACHE_MAX_KEY_LENGTH,
                                             default_key_func)
from django.utils.hashcompat import md5_constructor


def safe_cache_key(key, key_prefix, version):
    """Hashes cache keys that are longer than MEMCACHE_MAX_KEY_LENGTH chars."""
    result = default_key_func(key, key_prefix, version)
    if len(result) > MEMCACHE_MAX_KEY_LENGTH:
        result = md5_constructor(result).hexdigest()
    return result
