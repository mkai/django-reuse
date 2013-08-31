import re
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

