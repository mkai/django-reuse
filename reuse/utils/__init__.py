import os
import urllib2
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile


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


