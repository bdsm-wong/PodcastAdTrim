from server.app.Utils import ResponseHttp

class OptionalInputMiddleware:
    @staticmethod
    def invokable(request):
        data = request.form.to_dict()

        # Validate the format of 'show' (if present)
        show_data = data.get('show', [])
        if isinstance(show_data, str):
            try:
                eval(show_data)
            except Exception as e:
                return ResponseHttp.error_message_dictionary(message='Invalid format for "show". It should be an array.')

        # Validate the optionality and format of 'recorded_fragment_duration_min'
        recorded_fragment_duration_min = data.get('recorded_fragment_duration_min', 0)
        if not OptionalInputMiddleware.is_float(recorded_fragment_duration_min):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "recorded_fragment_duration_min". It should be a number or float.')

        # Validate the optionality and format of 'recorded_fragment_duration_max'
        recorded_fragment_duration_max = data.get('recorded_fragment_duration_max', None)
        if recorded_fragment_duration_max is not None and not OptionalInputMiddleware.is_float(recorded_fragment_duration_max):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "recorded_fragment_duration_max". It should be a number or float.')

        # Validate the optionality and format of 'min_average_fragment_amplitude'
        min_average_fragment_amplitude = data.get('min_average_fragment_amplitude', 0)
        if not OptionalInputMiddleware.is_float(min_average_fragment_amplitude):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "min_average_fragment_amplitude". It should be a number or float.')
        if not (0 <= float(min_average_fragment_amplitude) <= 1):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "min_average_fragment_amplitude". It should be a number or float between 0 and 1.')

        # Validate the optionality and format of 'max_average_fragment_amplitude'
        max_average_fragment_amplitude = data.get('max_average_fragment_amplitude', 1)
        if not OptionalInputMiddleware.is_float(max_average_fragment_amplitude):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "max_average_fragment_amplitude". It should be a number or float.')        
        if not (0 <= float(max_average_fragment_amplitude) <= 1):
            return ResponseHttp.error_message_dictionary(message='Invalid format for "max_average_fragment_amplitude". It should be a number or float between 0 and 1.')

        return {'error': False}
    
    @staticmethod
    def is_float(value):
        try:
            float(value)
            return True
        except ValueError:
            return False