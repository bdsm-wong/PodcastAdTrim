from flask import jsonify
import tempfile
import io
from ..Service import AudioProcessor
from ..Utils import ResponseHttp,AudioFormat

class AudioDetectionController:
    """
        {
            full_audio: audio_file,
            audio_fragment: audio_file,
            show: array[],
            (optional) recorded_fragment_duration_min: float,
            (optional) recorded_fragment_duration_max: float,
            (optional) min_average_fragment_amplitude: float,
            (optional) max_average_fragment_amplitude: float
        }
    """
    @staticmethod
    def invokable(request):
        try:
            data = request.form.to_dict()
            show_data = data.get('show', [])
            if isinstance(show_data, str):
                show_data = eval(show_data)

            recorded_fragment_duration_min = data.get('recorded_fragment_duration_min', 0)
            recorded_fragment_duration_max = data.get('recorded_fragment_duration_max', None)
            min_average_fragment_amplitude = data.get('min_average_fragment_amplitude', 0)
            max_average_fragment_amplitude = data.get('max_average_fragment_amplitude', 1)

            # Check if "full_audio" file or name is present
            type_full_audio = AudioFormat.request_type(request, key='full_audio')

            # Generate or look up file name for "full_audio" depending on type
            match type_full_audio:
                case 'file':
                    file_full_audio = request.files['full_audio']
                    full_audio_data = io.BytesIO(file_full_audio.read())
                    with tempfile.NamedTemporaryFile(delete=False) as temp_full_audio_file:
                        temp_full_audio_file.write(full_audio_data.read())
                        full_audio_file_name = temp_full_audio_file.name
                case 'name':
                    full_audio_file_name = f"full/{data.get('full_audio')}.npz"

            # Check if "audio_fragment" file or name is present
            type_audio_fragment = AudioFormat.request_type(request, key='audio_fragment')

            # Generate or look up file name for "audio_fragment" depending on type
            match type_audio_fragment:
                case 'file':
                    file_audio_fragment = request.files['audio_fragment']
                    audio_fragment = io.BytesIO(file_audio_fragment.read())
                    with tempfile.NamedTemporaryFile(delete=False) as temp_audio_fragment_file:
                        temp_audio_fragment_file.write(audio_fragment.read())
                        audio_fragment_file_name = temp_audio_fragment_file.name
                case 'name':
                    audio_fragment_file_name = f"frag/{data.get('audio_fragment')}.npz"

            audio_processor = AudioProcessor(movie_audio_filename=full_audio_file_name,
                                             sound_fragment_filename=audio_fragment_file_name,
                                             recorded_fragment_duration_min=recorded_fragment_duration_min,
                                             recorded_fragment_duration_max=recorded_fragment_duration_max,
                                             min_average_fragment_amplitude=min_average_fragment_amplitude,
                                             max_average_fragment_amplitude=max_average_fragment_amplitude
                                             )
            
            load_and_search_audio = audio_processor.load_and_search_audio(show_elements_array=show_data)
            
            if(load_and_search_audio['error']): return ResponseHttp.error_message(message=load_and_search_audio['message'],status_code=500)
            return ResponseHttp.successful_message(load_and_search_audio['message'])
        except Exception as e:
            return ResponseHttp.error_message(message=f'AudioDetectionController process_audio => {e}', status_code=500)