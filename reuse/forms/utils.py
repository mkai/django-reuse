from django.forms.forms import NON_FIELD_ERRORS
from django.forms.util import ErrorDict


def add_form_error(form, message, field=None):
    """
    Utility function to manually inject an error into a form.
    
    """
    if field:  # set a specific field's error
        form._errors[field] = form.error_class([message])
        return
    # set a non-field error
    if not form._errors:
        form._errors = ErrorDict()
    if not NON_FIELD_ERRORS in form._errors:
        form._errors[NON_FIELD_ERRORS] = form.error_class()
    form._errors[NON_FIELD_ERRORS].append(message)
