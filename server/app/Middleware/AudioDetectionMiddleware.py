from ..Utils import ResponseHttp, AudioFormat

class AudioDetectionMiddleware:
    @staticmethod
    def invokable(request):
        try:
            # Check if "full_audio" file or name is present
            type_full_audio = AudioFormat.request_type(request,key='full_audio')

            # Validate data depending on type
            match type_full_audio:
                case 'file':
                    file_full_audio = request.files['full_audio']
                    if not AudioFormat.validate_extension(file_full_audio.filename):
                        return ResponseHttp.error_message_dictionary(
                            message='Invalid format for "full_audio". Supported formats are: mp3, wav, m4a, ogg.')
                case 'name':
                    name_full_audio = request.form.get('full_audio')
                    if not isinstance(name_full_audio, str):
                        return ResponseHttp.error_message_dictionary(
                            message='If "full_audio" is not a file, it must be a string.')
                case _:
                    return ResponseHttp.error_message_dictionary(
                        message='"full_audio" file or name is required.')

            # Check if "audio_fragment" file or name is present
            type_audio_fragment = AudioFormat.request_type(request, key='audio_fragment')

            # Validate data depending on type
            match type_audio_fragment:
                case 'file':
                    file_audio_fragment = request.files['audio_fragment']
                    if not AudioFormat.validate_extension(file_audio_fragment.filename):
                        return ResponseHttp.error_message_dictionary(
                            message='Invalid format for "audio_fragment". Supported formats are: mp3, wav, m4a, ogg.')
                case 'name':
                    name_audio_fragment = request.form.get('audio_fragment')
                    if not isinstance(name_audio_fragment, str):
                        return ResponseHttp.error_message_dictionary(
                            message='If "audio_fragment" is not a file, it must be a string.')
                case _:
                    return ResponseHttp.error_message_dictionary(
                        message='"audio_fragment" file or name is required.')

            return {'error': False}
        except Exception as e:
            return ResponseHttp.error_message_dictionary(message=f'Error in AudioDetectionMiddleware: {str(e)}')