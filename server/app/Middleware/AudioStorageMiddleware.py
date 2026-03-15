from ..Utils import ResponseHttp, AudioFormat

class AudioStorageMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if "file_audio" is present
            if 'file_audio' not in request.files:
                return ResponseHttp.error_message_dictionary(message='"file_audio" file is required.')

            # Validate format for "file_audio"
            file_audio = request.files['file_audio']
            if not AudioFormat.validate_extension(file_audio.filename):
                return ResponseHttp.error_message_dictionary(message='Invalid format for "file_audio". Supported formats are: mp3, wav, m4a, ogg.')

            # Validate name_audio
            name_audio = request.form.get('name_audio')
            if name_audio is None or not isinstance(name_audio, str):
                return ResponseHttp.error_message_dictionary(message='Invalid or missing "name_audio". It should be a string.')

            # Validate type_audio
            type_audio = request.form.get('type_audio')
            audio_type_list = ['full', 'frag']
            if type_audio not in audio_type_list:
                return ResponseHttp.error_message_dictionary(message=f'Invalid or missing "type_audio". It should be in: {audio_type_list}')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')