import re
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.db import connection

qn = connection.ops.quote_name


def qf(table, field):  # quote table and field
    return '%s.%s' % (qn(table), qn(field))


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
    sql = '''SELECT COUNT(*) FROM %s WHERE %s=%%s AND %s=%s::text''' % (
        qn(comment_table),
        qf(comment_table, 'content_type_id'),
        qf(comment_table, 'object_pk'),
        qf(commented_table, 'id')
    )

    return queryset.extra(select={'comment_count': sql},
        select_params=(contenttype.pk, )
    )


def extract_mentioned_usernames(input_text):
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
    username_re = re.compile(r'^[\w.@+-]+')
    for mention in mentions:
        result = username_re.match(mention[1:])
        if result:
            usernames.append(result.group(0))
    return usernames
