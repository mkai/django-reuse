# A custom comments app that only supports registered users and therefore
# doesn't require a username string, an email address or URL to be given.
#
# Comment ownership can be determined from the user_id field.
# 
# From:
# http://blog.jvc26.org/2011/07/31/django-remove-excess-comment-fields

from django.contrib.comments.models import Comment
from reuse.apps.lightcomments.forms import LightCommentForm


def get_model():
    return Comment


def get_form():
    return LightCommentForm
