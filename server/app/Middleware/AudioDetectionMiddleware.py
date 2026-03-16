from ..Utils import ResponseHttp, AudioFormat

class AudioDetectionMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if "full_audio" file or name is present
            file_full_audio = request.files['full_audio']
            name_full_audio = request.form.get('full_audio')
            if file_full_audio is None and name_full_audio is None:
                return ResponseHttp.error_message_dictionary(
                    message='"full_audio" file or name is required.')

            # Validate "full_audio"
            if file_full_audio is not None:     # Use file if present
                if not AudioFormat.validate_extension(file_full_audio.filename):
                    return ResponseHttp.error_message_dictionary(
                        message='Invalid format for "full_audio". Supported formats are: mp3, wav, m4a, ogg.')
            else:       # Treat as a name if no file is passed in
                if not isinstance(name_full_audio, str):
                    return ResponseHttp.error_message_dictionary(
                        message='If "full_audio" is not a file, it must be a string.')

            # Check if "audio_fragment" file or name is present
            file_audio_fragment = request.files['audio_fragment']
            name_audio_fragment = request.form.get('audio_fragment')
            if file_audio_fragment is None and name_audio_fragment is None:
                return ResponseHttp.error_message_dictionary(
                    message='"audio_fragment" file or name is required.')

            # Validate "audio_fragment"
            if file_audio_fragment is not None:     # Use file if present
                if not AudioFormat.validate_extension(file_audio_fragment.filename):
                    return ResponseHttp.error_message_dictionary(
                        message='Invalid format for "audio_fragment". Supported formats are: mp3, wav, m4a, ogg.')
            else:       # Treat as a name if no file is passed in
                if not isinstance(name_audio_fragment, str):
                    return ResponseHttp.error_message_dictionary(
                        message='If "audio_fragment" is not a file, it must be a string.')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')