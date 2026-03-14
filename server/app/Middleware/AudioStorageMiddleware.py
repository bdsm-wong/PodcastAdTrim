from ..Utils import ResponseHttp, AudioFormat

class AudioStorageMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if both "full_audio" and "audio_fragment" files are present
            if 'full_audio' not in request.files:
                return ResponseHttp.error_message_dictionary(message='"full_audio" file are required.')

            # Validate format for "full_audio"
            file_full_audio = request.files['full_audio']
            if not AudioFormat.validate_extension(file_full_audio.filename):
                return ResponseHttp.error_message_dictionary(message='Invalid format for "full_audio". Supported formats are: mp3, wav, m4a, ogg.')

            # Validate name_full_audio
            name_full_audio = request.form.get('name_full_audio')
            if name_full_audio is None or not isinstance(name_full_audio, str):
                return ResponseHttp.error_message_dictionary(message='Invalid or missing "name_full_audio". It should be a string.')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')