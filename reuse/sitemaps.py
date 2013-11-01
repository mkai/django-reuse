import os
import datetime
from django.core import urlresolvers
from django.conf import settings
from django.contrib.sitemaps import Sitemap


# from: http://minimoesfuerzo.org/2011/02/12/sitemaps-django-static-pages/
class StaticSitemap(Sitemap):
    """Return the static sitemap items"""
    priority = 0.5

    def __init__(self, patterns, static_url_names=[]):
        self.patterns = patterns
        self._items = {}
        for pattern in self.patterns:
            name = getattr(pattern, 'name', None)
            if name is None:
                continue
            if name.startswith('static_') or name in static_url_names:
                self._items[name] = self._get_modification_date(pattern)

    def _get_modification_date(self, p):
        template = p.default_args.get('template')
        if template:
            template_path = self._get_template_path(template)
            mtime = os.stat(template_path).st_mtime
            mod_date = datetime.datetime.fromtimestamp(mtime)
        else:
            mod_date = None
        return mod_date

    def _get_template_path(self, template_path):
        for template_dir in settings.TEMPLATE_DIRS:
            path = os.path.join(template_dir, template_path)
            if os.path.exists(path):
                return path
        return None

    def items(self):
        return self._items.keys()

    def changefreq(self, obj):
        return 'monthly'

    def lastmod(self, obj):
        return self._items[obj]

    def location(self, obj):
        return urlresolvers.reverse(obj)
