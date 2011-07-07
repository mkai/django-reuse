from django import template
from jsmin import jsmin

register = template.Library()

class MinifyJs(template.Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist
    def render(self, context):
        return jsmin(self.nodelist.render(context))

def minifyjs(parser, token):
    nodelist = parser.parse(('endminifyjs',))
    parser.delete_first_token()
    return MinifyJs(nodelist)

minifyjs = register.tag(minifyjs)