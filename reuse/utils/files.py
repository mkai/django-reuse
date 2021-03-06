from __future__ import unicode_literals

import os
import logging
import mimetypes
import warnings
from django.core.files.temp import NamedTemporaryFile
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.utils.http import urlunquote
from . import max_field_length

try:
    from urlparse import urlsplit
except ImportError:
    from urllib.parse import urlsplit

logger = logging.getLogger(__name__)


def file_from_url(url):
    """Returns a file object from the data downloaded from the given URL."""
    try:
        import requests
    except ImportError:
        raise ImportError("file_from_url needs requests installed.")

    response = requests.get(url)
    return file_from_response(response)


def file_from_response(response):
    if response.status_code == 204:  # No content
        return None, None, None
    path = urlsplit(response.url).path
    name = urlunquote(os.path.basename(path))
    content_type = response.headers['content-type']
    # create temp file with the downloaded data
    temp_file = NamedTemporaryFile()
    temp_file.write(response.content)
    temp_file.size = len(response.content)
    temp_file.flush()
    temp_file.seek(0)
    return name, temp_file, content_type


def detect_file_mimetype(file):
    """Detects file mime type from file header."""
    try:
        import magic
    except ImportError:
        warnings.warn('detect_file_mimetype needs python-magic installed')
        return None

    try:
        mime = magic.from_buffer(file.read(1024), mime=True)
    except:
        return None
    else:
        return mime.decode(encoding='UTF-8')
    finally:
        file.seek(0)


def clean_filename(name, max_length=None, mimetype=None):
    if 'http' in name:  # g.etfv.co fix for filenames like 'http://www.ab.cd/'
        name = name.replace('.', '_')
    name = name.replace('/', '_').replace(':', '_')
    # guess extension from given mimetype
    if mimetype:
        ext = mimetypes.guess_extension(mimetype, strict=False)
        if ext:
            prefix = os.path.splitext(name)[0]
            name = (prefix or 'file') + ext
    # trim filename (from the front!) if needed
    if max_length:
        name = name[-max_length:]
    return name


def save_model_file(model_obj, field_name, filename, file, mimetype=None):
    # clean name
    max_len = max_field_length(model_obj, field_name)
    mimetype = mimetype or detect_file_mimetype(file)
    filename = clean_filename(filename, max_length=max_len, mimetype=mimetype)
    try:
        # set the file instance so that upload_to handlers can detect the
        # file extension from the content.
        wrapped_file = InMemoryUploadedFile(file, field_name, filename,
                                            content_type=None, size=0,
                                            charset=None)
        # save
        setattr(model_obj, field_name, wrapped_file)
        getattr(model_obj, field_name).file.seek(0)
        getattr(model_obj, field_name).save(filename, file, save=False)  # WTF?
    except Exception as e:
        raise IOError('Error while saving: {!r}'.format(e))


def save_model_image(model_obj, field_name, image_file, filename):
    # accept only images
    mimetype = detect_file_mimetype(image_file)
    if mimetype == 'application/x-empty':
        mimetype = None
    if mimetype and not mimetype.startswith('image/'):
        raise ValueError('Non-image mimetype "{}"'.format(mimetype))
    # check if the file can be read by PIL/ Pillow
    try:
        from PIL import Image
        Image.open(image_file)
    except ImportError:
        pass  # assume that user has PIL (needed for Django ImageField)
    except Exception as e:
        logger.debug('Couldn\'t read image file: {!r}'.format(e))
        raise IOError('File not readable: {!r}'.format(e))
    # save the image to storage
    save_model_file(model_obj, field_name, filename, image_file, mimetype)
