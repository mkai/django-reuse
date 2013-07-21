import hashlib
from django.core.cache.backends.base import (MEMCACHE_MAX_KEY_LENGTH,
                                             default_key_func)


def safe_cache_key(key, key_prefix, version):
    """Hashes cache keys that are longer than MEMCACHE_MAX_KEY_LENGTH chars."""
    result = default_key_func(key, key_prefix, version)
    if len(result) > MEMCACHE_MAX_KEY_LENGTH:
        result = hashlib.md5(result).hexdigest()
    return result
