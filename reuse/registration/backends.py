from django.conf import settings
from registration.backends.simple import SimpleBackend


class CustomRedirectRegistrationBackend(SimpleBackend):
    """
    A customized registration backends that changes the URL that a newly
    registered users gets redirected to.

    """
    def post_registration_redirect(self, request, user):
        """
        After registration, redirect to the URL given in the settings, or to
        the user's absolute_url if not given.

        """
        redirect_url = getattr(settings, 'REGISTRATION_REDIRECT_URL',
            user.get_absolute_url())
        return (redirect_url, (), {})
