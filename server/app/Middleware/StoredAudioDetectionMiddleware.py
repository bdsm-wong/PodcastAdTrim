from ..Utils import ResponseHttp, AudioFormat

class StoredAudioDetectionMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if both "audio_fragment" and "audio_fragment" files are present
            if 'audio_fragment' not in request.files:
                return ResponseHttp.error_message_dictionary(message='"audio_fragment" file are required.')

            # Validate format for "audio_fragment"
            file_audio_fragment = request.files['audio_fragment']
            if not AudioFormat.validate_extension(file_audio_fragment.filename):
                return ResponseHttp.error_message_dictionary(message='Invalid format for "audio_fragment". Supported formats are: mp3, wav, m4a, ogg.')

            # Validate name_full_audio
            name_full_audio = request.form.get('name_full_audio')
            if name_full_audio is None or not isinstance(name_full_audio, str):
                return ResponseHttp.error_message_dictionary(message='Invalid or missing "name_full_audio". It should be a string.')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')