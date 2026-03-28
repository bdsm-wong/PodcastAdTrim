import time
from .AudioProcessing import AudioLoader
from .AudioProcessing import AudioLocator
from ..Utils import AudioThresholdValidator, get_minutes_and_seconds
from dotenv import load_dotenv
import os

load_dotenv()

class AudioProcessor:
    def __init__(self, movie_audio_filename=None, sound_fragment_filename=None, logger=None,
                recorded_fragment_duration_min = 0, recorded_fragment_duration_max = None,
                min_average_fragment_amplitude = 0, max_average_fragment_amplitude = 1):
        self._movie_audio_filename = movie_audio_filename
        self._sound_fragment_filename = sound_fragment_filename
        self._logger = logger

        self._audio_loader = AudioLoader(movie_audio_filename=self._movie_audio_filename,
                                         sound_fragment_filename=self._sound_fragment_filename)
        self._audio_locator = None
        self._total_execution_time = 0

        self._recorded_fragment_duration_min = recorded_fragment_duration_min
        self._recorded_fragment_duration_max = recorded_fragment_duration_max
        self._min_average_fragment_amplitude = min_average_fragment_amplitude
        self._max_average_fragment_amplitude = max_average_fragment_amplitude

    def load_and_search_audio(self, show_elements_array = []):
        try:
            # ---- START TIME ----
            total_execution_time_start = time.time()

            # Load audio files
            audio_loader_data = self._audio_loader.load_audio_data()
            if audio_loader_data['error']: return audio_loader_data
            
            # validate fragment audio
            validate_fragment_audio = self._validate_fragment_audio()
            if validate_fragment_audio['error']: return validate_fragment_audio
        
            # Find Position
            self._audio_locator = AudioLocator(audio_loader=self._audio_loader)
            num_parts = int(os.getenv("NUM_PARTITIONS_CORRELATE", default=4))
            find_segment_audio = self._audio_locator.find_segment(num_parts=num_parts)
            if find_segment_audio['error']: return find_segment_audio

            #TODO - save correlate matrix to file

            # ---- FINISH TIME ----
            total_execution_time_end = time.time()
            self._total_execution_time = total_execution_time_end - total_execution_time_start

            #TODO - store results to database

            # Show elements
            return {
                'error': False,
                'message': self._show_elements(show_elements_array=show_elements_array)
            }
        
        except Exception as error:
            self._logger.error(str(error))
            return {
                "error": True,
                "message": f'Error loading an search audio: {str(error)}',
            }
    
    def _validate_fragment_audio(self):
        _frag_duration = self._audio_loader.frag_matrix.audio_duration
        if _frag_duration < float(self._recorded_fragment_duration_min):
            return {
                'error': True,
                'message': f'The duration of the audio fragment is less than the expected minimum duration. \
                Expected minimum duration: {self._recorded_fragment_duration_min}. \
                Actual duration: {_frag_duration}.'
            }
        
        if self._recorded_fragment_duration_max is not None and \
                _frag_duration > float(self._recorded_fragment_duration_max):
            return {
                'error': True,
                'message': f'The duration of the audio fragment is more than the expected maximum duration. \
                Expected maximum duration: {self._recorded_fragment_duration_max}. \
                Actual duration: {_frag_duration}.'
            }

        audio_threshold = AudioThresholdValidator.sound_threshold_limit(
            matrix_audio=self._audio_loader.frag_matrix.audio_matrix,
            min=self._min_average_fragment_amplitude,
            max=self._max_average_fragment_amplitude)
        if audio_threshold['error']: return audio_threshold
        self._fragment_average_threshold = audio_threshold['message']
        
        return {'error': False}
    
    def _show_elements(self, show_elements_array):
        elements = {'location_in_seconds': self._audio_locator.exact_second}
        if 'total_execution_time' in show_elements_array:
            elements['total_execution_time'] = self._total_execution_time

        if 'location_in_minutes' in show_elements_array:
            elements['location_in_minutes'] = get_minutes_and_seconds(self._audio_locator.exact_second)
        
        if 'recorded_fragment_length' in show_elements_array:
            elements['recorded_fragment_length'] = self._audio_loader.frag_matrix.duration

        if 'fragment_average_amplitude' in show_elements_array:
            elements['fragment_average_amplitude'] = self._fragment_average_threshold

        return elements