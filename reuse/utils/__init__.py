from datetime import datetime
from django import forms
from django.core.validators import validate_email
from django.shortcuts import _get_queryset
from django.utils import timezone

# timezone-aware 0-timestamp
TIMEZONE_EPOCH = timezone.make_aware(datetime(1970, 1, 1), timezone.utc)


def get_request_host(request):
    return 'http{}://{}'.format(('', 's')[request.is_secure()],
                                request.get_host())


def get_request_url(request):
    return request.build_absolute_uri(request.get_full_path())


def get_object_or_None(klass, *args, **kwargs):
    """
    Uses get() to return an object or None if the object does not exist.

    klass may be a Model, Manager, or QuerySet object. All other passed
    arguments and keyword arguments are used in the get() query.

    Note: Like with get(), a MultipleObjectsReturned will be raised if more than one
    object is found.

    From: django-annoying

    """
    queryset = _get_queryset(klass)
    try:
        return queryset.get(*args, **kwargs)
    except queryset.model.DoesNotExist:
        return None


def max_field_length(model, field_name):
    """Returns a model field's max_length."""
    return model._meta.get_field(field_name).max_length


def is_valid_email(val):
    try:
        validate_email(val)
        return True
    except forms.ValidationError:
        return False
