# source: http://djangosnippets.org/snippets/539/
from django import template

class AssignNode(template.Node):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        
    def render(self, context):
        context[self.name] = self.value.resolve(context, True)
        return ''

def do_assign(parser, token):
    """
    Assign an expression to a variable in the current context.
    
    Syntax::
        {% assign [name] [value] %}
    Example::
        {% assign list entry.get_related %}
        
    """
    bits = token.contents.split()
    # if len(bits) != 3:
        # raise template.TemplateSyntaxError("'%s' tag takes two arguments" % bits[0])
    varname = bits[1]
    value = " ".join(bits[2:])
    compiled_value = parser.compile_filter(value)
    return AssignNode(varname, compiled_value)

register = template.Library()
register.tag('assign', do_assign)
