from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
import urllib2
import os

"""

"""
def file_from_url(url):
    try:        
        request = urllib2.urlopen(url)
        
        temp_file = NamedTemporaryFile()
        temp_file.write(request.read())
        temp_file.flush()

        file_name = os.path.basename(request.geturl())                
        file_instance = File(temp_file)
        
        return file_name, file_instance
    except Exception:
        raise
