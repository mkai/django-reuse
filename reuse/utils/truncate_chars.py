# source: http://code.djangoproject.com/ticket/5025
from django.utils.functional import allow_lazy 
from django.utils.encoding import force_unicode 
from django.utils.translation import ugettext as _
import unicodedata


def truncate_chars(s, num, end_text='...'):
    """
    Truncates a string after a certain number of characters. Takes an
    optional argument of what should be used to notify that the string has been
    truncated, defaulting to ellipsis (...)
    
    """
    s = force_unicode(s)
    length = int(num)
    
    normalized = unicodedata.normalize('NFC', s)
    
    # If the text is short enough, we can bail out right now
    if len(normalized) <= length:
        return normalized
    
    translated_end_text = _(end_text)
    len_end_text = len(translated_end_text)
    
    end_index = max(length - len_end_text, 0)
    while unicodedata.combining(
        normalized[end_index]) and end_index < len(normalized):
        end_index += 1
    
    return u'%s%s' % (normalized[:end_index], translated_end_text)
truncate_chars = allow_lazy(truncate_chars, unicode)
