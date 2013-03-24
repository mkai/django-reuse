# Adapted from:
# https://github.com/omab/django-social-auth/issues/46#issuecomment-3331082
import json
import urllib
import urllib2
from django.template.defaultfilters import slugify
from django.conf import settings
from social_auth.backends.google import (BACKENDS, GoogleOAuth2,
                                         GoogleOAuth2Backend)


class GoogleProfileBackend(GoogleOAuth2Backend):
    """
    A Google OAuth2 authentication backend that also retrieves the user's
    Google ID, email, as well as some profile info.

    """
    name = 'google'

    def get_user_id(self, details, response):
        """
        Associate the user by numeric Google ID, not email address.

        """
        return details['id']

    def get_user_details(self, response):
        """
        Return user details from Google account

        """
        # if the response contains the full name, use the slugified full name
        # as the user name, otherwise use the user part of the email address
        email = response['email']
        username = email.split('@', 1)[0]
        if response.get('name', False) and not '@' in response['name']:
            username = slugify(response['name'])

        return {
            'id': response['id'],
            'username': username,
            'email': email,
            'fullname': response.get('name', ''),
            'first_name': response.get('given_name', ''),
            'last_name': response.get('family_name', ''),
            'gender': response.get('gender', ''),
        }


class GoogleProfile(GoogleOAuth2):
    """
    Google OAuth2 support

    """
    AUTH_BACKEND = GoogleProfileBackend

    def get_scope(self):
        scope = [
            'https://www.googleapis.com/auth/userinfo.email',
            'https://www.googleapis.com/auth/userinfo.profile',
        ]
        return scope + getattr(settings, 'GOOGLE_OAUTH_EXTRA_SCOPE', [])

    def user_data(self, access_token, *args, **kwargs):
        """Return user data from Google API."""
        return self.googleapis_profile(
            'https://www.googleapis.com/oauth2/v1/userinfo', access_token)

    def googleapis_profile(self, url, access_token):
        """
        Loads user data from googleapis service

        Google OAuth documentation at:
            http://code.google.com/apis/accounts/docs/OAuth2Login.html

        """
        data = {'access_token': access_token, 'alt': 'json'}
        request = urllib2.Request(url + '?' + urllib.urlencode(data))
        try:
            return json.loads(urllib2.urlopen(request).read())
        except (ValueError, KeyError, IOError):
            return None

BACKENDS['google'] = GoogleProfile
