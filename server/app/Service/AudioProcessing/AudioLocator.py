from scipy import signal
import numpy as np
import logging

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)

class AudioLocator:

    def __init__(self, audio_loader):
        self.__exact_minutes = []
        self.__max_correlations = []

        self.__audio_matrix = audio_loader.audio_matrix
        self.__sample_rate = audio_loader.sample_rate
        self.__audio_duration = audio_loader.audio_duration
        self.__audio_fragment_matrix = audio_loader.audio_fragment_matrix

    def find_segment(self, num_parts = 4):
        try:
            part_length = len(self.__audio_matrix) // num_parts
            
            for part_number in range(1, num_parts + 1):
                correlate_data = self._correlate(part_length=part_length, part_number=part_number)
                if(correlate_data['error']): return correlate_data
                
                exact_minute = correlate_data['message']['exact_second']
                max_correlation = correlate_data['message']['max_correlation']

                self.__exact_minutes.append(exact_minute)
                self.__max_correlations.append(max_correlation)
           
            
            max_correlation_index = self.__max_correlations.index(max(self.__max_correlations))
            minute_registered_array = self.__exact_minutes[max_correlation_index]
            
            relative_exact_minute = (self.__audio_duration * max_correlation_index / num_parts) + minute_registered_array

            return {"error": False,
                    "message": relative_exact_minute
                    }
        except Exception as error:
            return {
                "error": True,
                "message": f'Error finding segment: {str(error)}',
            }

    def _correlate(self, part_length, part_number=1):
        try:
            start = (part_number - 1) * part_length
            end = part_number * part_length
            audio_fragment_matrix_part = self.__audio_matrix[start:end]

            correlation = signal.correlate(audio_fragment_matrix_part, self.__audio_fragment_matrix, mode='valid', method='fft')

            peak = np.argmax(correlation)
            exact_second = peak / self.__sample_rate
            max_correlation = np.max(correlation)

            return {"error": False,
                    "message": {
                        'exact_second': exact_second,
                        'max_correlation': max_correlation,
                    }}
        except Exception as error:
            return {
                "error": True,
                "message": f'Error in correlation: {str(error)}',
            }