from __future__ import unicode_literals

import re
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.db.connection.ops import quote_name as _qn


def _qf(table, field):  # quote table and field
    return '{}.{}'.format(_qn(table), _qn(field))


def annotate_with_comment_count(queryset):
    """
    Annotate queryset with comment count

    From: http://djangosnippets.org/snippets/1101/

    """
    commented_model = queryset.model
    contenttype = ContentType.objects.get_for_model(commented_model)
    commented_table = commented_model._meta.db_table
    comment_table = Comment._meta.db_table

    # NOTE: ::text is specific to PostgreSQL
    sql = 'SELECT COUNT(*) FROM %s WHERE %s=%%s AND %s=%s::text' % (
        _qn(comment_table),
        _qf(comment_table, 'content_type_id'),
        _qf(comment_table, 'object_pk'),
        _qf(commented_table, 'id')
    )

    return queryset.extra(select={'comment_count': sql},
                          select_params=(contenttype.pk,))


def extract_mentioned_usernames(input_text,
                                username_re=re.compile(r'^[\w.@+-]+$')):
    """
    Parses a block of text for '@username' mentions and returns a list of
    user names mentioned in the text.

    """
    words = input_text.split(' ')
    mentions = [w for w in words if w.startswith('@')]  # '@ijonTichy'
    if not mentions:
        return []
    # collect user names, stripping out any punctuation chars.
    usernames = []
    for mention in mentions:
        result = username_re.match(mention[1:])
        if result:
            usernames.append(result.group(0))
    return usernames
