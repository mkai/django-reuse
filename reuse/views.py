from __future__ import unicode_literals

from django.conf import settings


class PaginationMixin(object):
    """
    A mixin for Django's ListView that sets project-wide values for pagination
    behaviour.

    """
    paginate_by = getattr(settings, 'PAGINATION_OBJECTS_PER_PAGE', 10)

    def get_paginator(self, queryset, *args, **kwargs):
        per_page = self.get_paginate_by(queryset)
        orphans = getattr(settings, 'PAGINATION_ORPHANS', 0)
        allow_empty_first_page =\
            getattr(settings, 'PAGINATION_ALLOW_EMPTY_FIRST_PAGE', True)
        return super(PaginationMixin, self).get_paginator(queryset, per_page,
                                                          orphans,
                                                          allow_empty_first_page)
