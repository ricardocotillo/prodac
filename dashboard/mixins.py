import json
from django.contrib.messages.api import get_messages
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse, HttpResponse

class JsonResponseMixin(object):
    """ Ajax form based on the django docs example.
    
    https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-editing/#ajax-example
    https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/#more-than-just-html
    """

    def set_success_messages(self):
        pass

    def set_error_messages(self):
        pass

    def get_response_data(self):
        data = {}
        if hasattr(self, 'object'):
            data['pk'] = self.object.pk
        return data

    def get_response_messages(self):
        msgs = []
        storage = get_messages(self.request)
            
        for m in storage:
            msgs.append({
                'message': m.message,
                'level': m.level,
                'tags': m.tags,
                'extra_tags': m.extra_tags,
                'level_tag': m.level_tag,
            })

        return msgs
    
    def form_invalid(self, form):
        if hasattr(super(), 'form_invalid'):
            response = super().form_invalid(form)
        else:
            response = HttpResponse()
        self.set_error_messages()
        if self.request.accepts('application/json'):
            return JsonResponse({
                'errors': form.errors,
                'messages': self.get_response_messages()
            }, status=400)
        return response

    def form_valid(self, form):
        if hasattr(super(), 'form_valid'):
            response = super().form_valid(form)
        else:
            response = HttpResponse()
        self.set_success_messages()
        if self.request.accepts('application/json'):
            # Request is ajax, send a json response
            res_data = {
                'data': self.get_response_data(),
                'messages': self.get_response_messages(),
            }
            return JsonResponse(res_data)
        return response


class FragmentsResponseMixin(object):
    """ Ajax form based on the django docs example.
    
    https://docs.djangoproject.com/en/dev/topics/class-based-views/generic-editing/#ajax-example
    https://docs.djangoproject.com/en/dev/topics/class-based-views/mixins/#more-than-just-html
    """
    success_message = 'Success'

    def render_to_json_response(self, context, **response_kwargs):
        """Render a json response of the context."""

        data = json.dumps(context)
        response_kwargs['content_type'] = 'application/json'
        return HttpResponse(data, **response_kwargs)
    
    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.accepts('application/json'):
            return render(self.request, 'components/alerts/messages.html', {'form': form})

        return response

    def form_valid(self, form):
        response = super().form_valid(form)
        if self.request.accepts('application/json'):
            return render(self.request, 'components/alerts/messages.html')

        return response