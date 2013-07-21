import os
import requests
import urlparse
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.utils.http import urlunquote


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
