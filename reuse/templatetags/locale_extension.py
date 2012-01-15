from django import template
import settings

register = template.Library()


@register.filter()
def full_locale(value):
    """
    Extends a language code to a full locale name with language specifier,
    with languages used as defined in settings.
    
    """
    lang_code = value[0:2]
    # fail deliberately when no extension in settings
    return settings.COUNTRY_EXTENSION[lang_code]
