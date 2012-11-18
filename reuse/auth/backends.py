"""
@author: chris http://djangosnippets.org/snippets/1845/
updated to 1.3 by Lukasz Kidzinski
source: http://djangosnippets.org/snippets/2463/
"""
from django.contrib.auth.models import User
from django.core.validators import email_re


class EmailBackend(object):
    """
    Authenticate with e-mail.

    Use the e-mail, and password

    Should work with django 1.3
    """

    supports_object_permissions = False
    supports_anonymous_user = False
    supports_inactive_user = False

    def _get_user_by_email(self, email):
        return User.objects.get(email=email)

    def authenticate(self, username=None, password=None):
        if email_re.search(username):
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
