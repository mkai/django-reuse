# source: http://djangosnippets.org/snippets/10/
from django import template

register = template.Library()

class CatchNode(template.Node):
    def __init__(self, nodelist, var_name):
        self.nodelist = nodelist
        self.var_name = var_name
        
    def render(self, context):
        output = self.nodelist.render(context)
        context[self.var_name] = output
        return ''

def do_catch(parser, token):
    """
    Catch the content and save it to var_name

    Example::

        {% catch as var_name %} ... {% endcatch %}
    """
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError, "%r tag requires arguments" % token.contents[0]
    m = re.search(r'as (\w+)', arg)
    if not m:
        raise template.TemplateSyntaxError, '%r tag should define as "%r as var_name"' % (tag_name, tag_name)
    var_name = m.groups()[0]
    nodelist = parser.parse(('endcatch',))
    parser.delete_first_token()
    return CatchNode(nodelist, var_name)
do_catch = register.tag('catch', do_catch)
