from django.shortcuts import render_to_response
from django.template import loader


def render_custom_response(*args, **kwargs):
    response = kwargs.pop('response')
    if not response:
        return render_to_response(*args, **kwargs)
    else:
        response.content = loader.render_to_string(*args, **kwargs)
        return response
