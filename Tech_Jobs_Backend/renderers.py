from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context['response'].status_code if renderer_context else 200

        # Don't wrap if it's already wrapped
        if isinstance(data, dict) and 'success' in data:
            return super().render(data, accepted_media_type, renderer_context)

        response = {
            'success': True if status_code < 400 else False,
            'message': 'Success' if status_code < 400 else 'Validation failed',
        }
        
        if status_code < 400:
            if data is not None:
                response['data'] = data
        else:
            response['errors'] = data

        return super().render(response, accepted_media_type, renderer_context)
