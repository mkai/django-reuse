from django.conf import settings
from django.utils.encoding import force_unicode
from django.utils.timezone import now
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.forms import CommentForm


class LightCommentForm(CommentForm):
    """
    A lighter comment form.
    
    """
    def get_comment_create_data(self):
        """
        This needs to be overwritten to remove the fields from the class
        """
        return dict(
            content_type=ContentType.objects.get_for_model(self.target_object),
            object_pk=force_unicode(self.target_object._get_pk_val()),
            comment=self.cleaned_data["comment"],
            submit_date=now(),
            site_id=settings.SITE_ID,
            is_public=True,
            is_removed=False,
        )
    
LightCommentForm.base_fields.pop('email')
LightCommentForm.base_fields.pop('url')
