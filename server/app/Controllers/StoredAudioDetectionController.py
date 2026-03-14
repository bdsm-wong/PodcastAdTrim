from flask import jsonify
import tempfile
import io
from server.app.Service import AudioProcessor
from server.app.Utils import ResponseHttp

class StoredAudioDetectionController:
    """
        {
            name_full_audio: string (The name of the .npz file you want to compare)
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

            name_full_audio = f"{data.get('name_full_audio')}.npz"

            file_audio_fragment = request.files['audio_fragment']
            audio_fragment = io.BytesIO(file_audio_fragment.read())
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_fragment_file:
                    temp_audio_fragment_file.write(audio_fragment.read())
                    temp_audio_fragment_file_name = temp_audio_fragment_file.name
            

            audio_processor = AudioProcessor(movie_audio_filename=name_full_audio, 
                                             sound_fragment_filename=temp_audio_fragment_file_name,
                                             recorded_fragment_duration_min=recorded_fragment_duration_min,
                                             recorded_fragment_duration_max=recorded_fragment_duration_max,
                                             min_average_fragment_amplitude=min_average_fragment_amplitude,
                                             max_average_fragment_amplitude=max_average_fragment_amplitude
                                             )
            
            load_and_search_audio = audio_processor.load_and_search_audio(show_elements_array=show_data)
            
            if(load_and_search_audio['error']): return ResponseHttp.error_message(message=load_and_search_audio['message'],status_code=500)
            return ResponseHttp.successful_message(load_and_search_audio['message'])
        except Exception as e:
            return ResponseHttp.error_message(message=f'StoredAudioDetectionController process_audio => {e}', status_code=400)