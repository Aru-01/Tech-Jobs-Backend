from rest_framework.renderers import JSONRenderer

class CustomJSONRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        response = renderer_context.get('response') if renderer_context else None
        status_code = response.status_code if response else 200

        # If data is already in our format, just return it
        if isinstance(data, dict) and 'success' in data:
            return super().render(data, accepted_media_type, renderer_context)

        # Standardize the response format
        formatted_data = {
            'success': True if status_code < 400 else False,
            'message': 'Success' if status_code < 400 else 'Error',
        }

        if status_code < 400:
            formatted_data['data'] = data
        else:
            # Handle error data (it could be a list, dict, or string)
            if isinstance(data, dict):
                formatted_data['errors'] = data
                if 'detail' in data:
                    formatted_data['message'] = data['detail']
            else:
                formatted_data['errors'] = data

        return super().render(formatted_data, accepted_media_type, renderer_context)
