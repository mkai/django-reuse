def render_custom_response(*args, **kwargs):
        response = kwargs.pop('response', None)
        
        if response == None:
            from django.shortcuts import render_to_response
            
            return render_to_response(*args, **kwargs)
        
        else:
            from django.template import loader
            response.content = loader.render_to_string(*args, **kwargs)
            
            return response
