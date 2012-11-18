from datetime import datetime, timedelta
from django.utils.translation import ugettext_lazy as _
from django_filters import CharFilter, DateRangeFilter, MultipleChoiceFilter


class CustomDateRangeFilter(DateRangeFilter):
    """
    A filter for ``django_filters`` that keeps only objects created in the past
    n days rather than objects in the last week (the original
    ``DateRangeFilter`` would potentially return 0 items on a Monday).

    """
    options = {
        '': (_('Any Date'), lambda qs, name: qs.all()),
        'today': (_('Today'), lambda qs, name: qs.filter(**{
            '%s__year' % name: datetime.today().year,
            '%s__month' % name: datetime.today().month,
            '%s__day' % name: datetime.today().day
        })),
        'lastweek': (_('Past 7 days'), lambda qs, name: qs.filter(**{
            '%s__gte' % name: (datetime.today() - timedelta(days=7)).strftime(
                '%Y-%m-%d'),
            '%s__lt' % name: (datetime.today() + timedelta(days=1)).strftime(
                '%Y-%m-%d'),
        })),
        'lastmonth': (_('Past 30 days'), lambda qs, name: qs.filter(**{
            '%s__gte' % name: (datetime.today() - timedelta(days=30)).strftime(
                '%Y-%m-%d'),
            '%s__lt' % name: (datetime.today() + timedelta(days=30)).strftime(
                '%Y-%m-%d'),
        })),
        'thisyear': (_('This year'), lambda qs, name: qs.filter(**{
            '%s__year' % name: datetime.today().year,
        })),
    }

    def filter(self, qs, value):
        if value not in self.options.keys():
            value = ''
        return self.options[value][1](qs, self.name)


class ExclusiveMultipleChoiceFilter(MultipleChoiceFilter):
    """
    A filter for ``django_filters`` that performs an AND query on the selected
    options.

    """
    def filter(self, qs, values):
        values = values or ()
        # TODO: this is a bit of a hack, but ModelChoiceIterator doesn't have a
        # __len__ method
        if len(values) == len(list(self.field.choices)):
            return qs
        for value in values:
            qs = qs.filter(**{'%s__%s' % (self.name, self.lookup_type): value})
        return qs


class OptionalMultipleChoiceFilter(MultipleChoiceFilter):
    """
    A filter for ``django_filters`` that doesn't filter the queryset if the
    value is an empty string.

    """
    def filter(self, qs, value):
        value = value or ()
        if len(value) == 1 and not value[0]:
            return qs
        return super(OptionalMultipleChoiceFilter, self).filter(qs, value)


class ExcludingCharFilter(CharFilter):
    """
    A filter for ``django_filters`` that allows for excluding objects
    containing specific keywords that start with a minus (e. g. in a search:
    "sweets -cookies" would return sweets, but not cookies).

    """
    def filter(self, qs, value):
        words = value.split(' ')
        exclusions = [w for w in words if w.startswith('-')]
        for excl in exclusions:
            value = value.replace(excl, '').strip()
            value = ' '.join(value.split())  # remove multiple whitespaces
            qs = qs.exclude(**{
                '%s__%s' % (self.name, self.lookup_type): excl[1:]
            })
        return super(ExcludingCharFilter, self).filter(qs, value)
