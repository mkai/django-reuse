def when_developing(view):
    """
    Usage:

    @when_developing
    def delete_all_users(request):
        User.objects.all().delete()
        return HttpResponse('Successfully deleted all users.')
    """

    from django.conf import settings

    def f404(*args, **kwargs):
        from django.http import Http404
        raise Http404

    def inner(*args, **kwargs):
        return view(*args, **kwargs)

    if not settings.DEBUG:
        return f404
    return inner
