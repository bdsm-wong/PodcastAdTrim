import time
from .AudioProcessing import AudioLoader
from .AudioProcessing import AudioLocator
from ..Utils import AudioThresholdValidator, get_minutes_and_seconds
import logging
from dotenv import load_dotenv
import os

load_dotenv()

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)

class AudioProcessor:
    def __init__(self, movie_audio_filename=None, sound_fragment_filename=None, custom_path=False,
                recorded_fragment_duration_min = 0, recorded_fragment_duration_max = None,
                min_average_fragment_amplitude = 0, max_average_fragment_amplitude = 1):
        self._movie_audio_filename = movie_audio_filename
        self._sound_fragment_filename = sound_fragment_filename
        self._custom_path = custom_path

        self._recorded_fragment_duration_min = recorded_fragment_duration_min
        self._recorded_fragment_duration_max = recorded_fragment_duration_max
        self._min_average_fragment_amplitude = min_average_fragment_amplitude
        self._max_average_fragment_amplitude = max_average_fragment_amplitude

    def load_and_search_audio(self, show_elements_array = []):
        try:
            # ---- START TIME ----
            total_execution_time_start = time.time()

            # Load audio files
            self._audio_loader = AudioLoader(movie_audio_filename=self._movie_audio_filename, 
                                        sound_fragment_filename=self._sound_fragment_filename,
                                        custom_path=self._custom_path)
            audio_loader_data = self._audio_loader.load_audio_data()
            if(audio_loader_data['error']): return audio_loader_data
            
            # validate fragment audio
            validate_fragment_audio = self._validate_fragment_audio()
            if(validate_fragment_audio['error']): return validate_fragment_audio
        
            # Find Position
            audio_locator = AudioLocator(audio_loader=self._audio_loader)
            self._find_segment_audio = audio_locator.find_segment(int(os.getenv("NUM_PARTITIONS_CORRELATE", default=4)))
            if(self._find_segment_audio['error']): return self._find_segment_audio
            
            # ---- FINISH TIME ----
            total_execution_time_end = time.time()
            self._total_execution_time = total_execution_time_end - total_execution_time_start
            
            # Show elements
            return {
                'error': False,
                'message': self._show_elements(show_elements_array=show_elements_array)
            }
        
        except Exception as error:
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error loading an search audio: {str(error)}',
            }
    
    def _validate_fragment_audio(self):
        if self._audio_loader.fragment_audio_duration < float(self._recorded_fragment_duration_min):
            return {
                'error': True,
                'message': f'The duration of the audio fragment is less than the expected minimum duration. Expected minimum duration: {self._recorded_fragment_duration_min}. Actual duration: {self._audio_loader.fragment_audio_duration}.'
            }
        
        if self._recorded_fragment_duration_max is not None and self._audio_loader.fragment_audio_duration > float(self._recorded_fragment_duration_max):
            return {
                'error': True,
                'message': f'The duration of the audio fragment is more than the expected maximum duration. Expected maximum duration: {self._recorded_fragment_duration_max}. Actual duration: {self._audio_loader.fragment_audio_duration}.'
            }
        
        
        audio_threshold = AudioThresholdValidator.sound_threshold_limit(matrix_audio=self._audio_loader.audio_fragment_matrix,
                                                      min=self._min_average_fragment_amplitude,
                                                      max=self._max_average_fragment_amplitude)
        if(audio_threshold['error']): return audio_threshold
        self._fragment_average_threshold = audio_threshold['message']
        
        return {'error': False}
    
    def _show_elements(self, show_elements_array):
        elements = {'location_in_seconds': self._find_segment_audio['message']}
        if 'total_execution_time' in show_elements_array:
            elements['total_execution_time'] = self._total_execution_time
        
        if 'location_in_minutes' in show_elements_array:
            elements['location_in_minutes'] = get_minutes_and_seconds(self._find_segment_audio['message'])
        
        if 'recorded_fragment_length' in show_elements_array:
            elements['recorded_fragment_length'] = self._audio_loader.fragment_audio_duration

        if 'fragment_average_amplitude' in show_elements_array:
            elements['fragment_average_amplitude'] = self._fragment_average_threshold

        return elements