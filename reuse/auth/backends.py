from django.contrib.auth.models import User
from django.contrib.auth.backends import ModelBackend # default backend
from django.core.validators import email_re

# Overwrite the default backend to check for e-mail address 
# Source: http://www.davidcramer.net/code/224/logging-in-with-email-addresses-in-django.html
class EmailBackend(ModelBackend):
    def authenticate(self, username=None, password=None):
        #If username is an email address, then try to pull it up
        if email_re.search(username):
            try:
                user = User.objects.get(email=username)
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
