from ..Utils import ResponseHttp, AudioFormat

class AudioDetectionMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if both "full_audio" and "audio_fragment" files are present
            if 'full_audio' not in request.files or 'audio_fragment' not in request.files:
                return ResponseHttp.error_message_dictionary(message='Both "full_audio" and "audio_fragment" files are required.')

            # Validate format for "full_audio"
            file_full_audio = request.files['full_audio']
            if not AudioFormat.validate_extension(file_full_audio.filename):
                return ResponseHttp.error_message_dictionary(message='Invalid format for "full_audio". Supported formats are: mp3, wav, m4a, ogg.')

            # Validate format for "audio_fragment"
            file_audio_fragment = request.files['audio_fragment']
            if not AudioFormat.validate_extension(file_audio_fragment.filename):
                return ResponseHttp.error_message_dictionary(message='Invalid format for "audio_fragment". Supported formats are: mp3, wav, m4a, ogg.')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')