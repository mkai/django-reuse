import re
from django import template

register = template.Library()


@register.filter
def replace(value, args):
    """
    Performs a regular expression search/replace on a string in your template.

    {% load replace %} {{ mystring|replace:"/l(u+)pin/m\1gen" }}

    If: mystring = 'lupin, luuuuuupin, and luuuuuuuuuuuuupin are le pwn'
    then it will return: mugen, muuuuuugen, and muuuuuuuuuuuuugen are le pwn

    The argument is in the following format:

    [delim char]regexp search[delim char]regexp replace

    From: http://djangosnippets.org/snippets/60/

    """
    args = args.split(args[0])
    search = args[1]
    replace = args[2]
    return re.sub(search, replace, value)
