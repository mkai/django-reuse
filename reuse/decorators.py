from functools import wraps
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.decorators import available_attrs


def logout_required(function=None, redirect_url=None):
    """
    Requires a logged-out user to view a URL, otherwise redirects the user to
    to the given *redirect_url*.

    """
    def decorator(view_func):
        @wraps(view_func, assigned=available_attrs(view_func))
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated():
                return view_func(request, *args, **kwargs)
            else:
                if redirect_url:
                    return HttpResponseRedirect(redirect_url)
                return HttpResponse(u'You need to be logged out to do this.')
        return _wrapped_view
    if function:
        return decorator(function)
    return decorator
