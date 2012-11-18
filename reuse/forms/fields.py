import re
from django.core.validators import email_re
from django.forms import CharField, Textarea, ValidationError
from django.utils.translation import ugettext as _

email_separator_re = re.compile(r'[^\w\.\-\+@_]+')


class MultipleEmailField(CharField):
    """
    A form field that validates a textarea containing multiple email addresses
    separated by commas or newlines.

    Adapted from: http://djangosnippets.org/snippets/1958/

    """
    widget = Textarea

    def clean(self, value):
        super(MultipleEmailField, self).clean(value)
        emails = email_separator_re.split(value)
        if not emails:
            raise ValidationError(_(u'Enter at least one e-mail address.'))
        for email in emails:
            if not email.strip():
                continue  # skip empty "addresses"
            if not email_re.match(email):
                error_msg = _(u'%s is not a valid e-mail address.') % email
                raise ValidationError(error_msg)
        return emails
