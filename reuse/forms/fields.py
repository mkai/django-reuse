import re
import json
from django import forms
from django.db import models
from django.core.validators import validate_email
from django.utils.translation import ugettext_lazy as _

email_separator_re = re.compile(r'[^\w\.\-\+@_]+')


class MultipleEmailField(forms.CharField):
    """
    A form field that validates a textarea containing multiple email addresses
    separated by commas or newlines.

    Adapted from: http://djangosnippets.org/snippets/1958/

    """
    widget = forms.Textarea

    def clean(self, value):
        super(MultipleEmailField, self).clean(value)
        emails = email_separator_re.split(value)
        if not emails:
            raise forms.ValidationError(_('Enter at least one e-mail address.'))
        for email in emails:
            if not email.strip():
                continue  # skip empty "addresses"
            try:
                validate_email(email)
            except forms.ValidationError:
                error_msg = _(u'%s is not a valid e-mail address.' % email)
                raise forms.ValidationError(error_msg)
        return emails


class URLTextField(models.TextField):
    """A URLField with an unlimited max_length."""
    description = _("URL")

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.URLField,
            'widget': forms.TextInput,
        }
        defaults.update(kwargs)
        return super(URLTextField, self).formfield(**defaults)


#######################
### Lazy JSON field ###
#######################
class Creator(object):
    """Taken from django.db.models.fields.subclassing."""
    _parent_key = '_json_field_cache'

    def __init__(self, field):
        self.field = field

    def __get__(self, obj, type=None):
        if obj is None:
            raise AttributeError('Can only be accessed via an instance.')

        cache = getattr(obj, self._parent_key, None)
        if cache is None:
            cache = {}
            setattr(obj, self._parent_key, cache)

        key = '%s_deserialized' % self.field.name

        if cache.get(key, False):
            return obj.__dict__[self.field.name]

        value = self.field.to_python(obj.__dict__[self.field.name])
        obj.__dict__[self.field.name] = value
        cache[key] = True

        return value

    def __set__(self, obj, value):
        obj.__dict__[self.field.name] = value  # deserialized when accessed


class LazyJSONField(models.TextField):
    """Stores and loads valid JSON objects lazily."""
    description = 'JSON object'

    def __init__(self, *args, **kwargs):
        self.default_error_messages = {
            'invalid': _(u'Enter a valid JSON object')
        }
        self._db_type = kwargs.pop('db_type', None)
        self.evaluate_formfield = kwargs.pop('evaluate_formfield', False)

        kwargs['default'] = kwargs.get('default', 'null')
        kwargs['help_text'] = kwargs.get('help_text',
                                         self.default_error_messages['invalid'])

        super(LazyJSONField, self).__init__(*args, **kwargs)

    def db_type(self, *args, **kwargs):
        if self._db_type:
            return self._db_type
        return super(LazyJSONField, self).db_type(*args, **kwargs)

    def to_python(self, value):
        if value is None:  # allow blank objects
            return None
        if isinstance(value, basestring):
            try:
                value = json.loads(value)
            except ValueError:
                pass
        return value

    def get_db_prep_value(self, value, *args, **kwargs):
        if self.null and value is None and not kwargs.get('force'):
            return None
        return json.dumps(value)

    def value_to_string(self, obj):
        return self.get_db_prep_value(self._get_val_from_obj(obj))

    def value_from_object(self, obj):
        return json.dumps(super(LazyJSONField, self).value_from_object(obj))

    def contribute_to_class(self, cls, name):
        super(LazyJSONField, self).contribute_to_class(cls, name)

        def get_json(model_instance):
            return self.get_db_prep_value(
                getattr(model_instance, self.attname, None), force=True)

        setattr(cls, 'get_%s_json' % self.name, get_json)

        def set_json(model_instance, value):
            return setattr(model_instance, self.attname, self.to_python(value))

        setattr(cls, 'set_%s_json' % self.name, set_json)
        setattr(cls, name, Creator(self))  # deferred deserialization
