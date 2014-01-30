"""
@author: chris http://djangosnippets.org/snippets/1845/
updated to 1.3 by Lukasz Kidzinski
Original source: http://djangosnippets.org/snippets/2463/
"""
from __future__ import unicode_literals

from django.contrib.auth import get_user_model
from ..utils import is_valid_email

User = get_user_model()


class EmailBackend(object):
    """Authenticate users with their e-mail address and password."""
    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def _get_user_by_email(self, email):
        return User.objects.get(email=email)

    def authenticate(self, username=None, password=None):
        if is_valid_email(username):
            try:
                user = self._get_user_by_email(username)
            except User.DoesNotExist:
                return None
        else:
            #We have a non-email address username we should try username
            try:
                user = User.objects.get(username=username)
            except User.DoesNotExist:
                return None
        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


class CaseInsensitiveEmailBackend(EmailBackend):
    """
    Same as EmailBackend, but allows arbitrary casing of the email address,
    e. g. Bob@examPle.com is as valid as bob@example.com.

    """
    def _get_user_by_email(self, email):
        return User.objects.get(email__iexact=email)
