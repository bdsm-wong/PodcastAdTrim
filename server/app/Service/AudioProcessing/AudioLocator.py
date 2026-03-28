from scipy import signal
import numpy as np
import logging

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)
#TODO - add timestamp to log entry
#TODO - set up single logging object, pass to subroutines as needed
#TODO - or log to DB?

class AudioLocator:

    def __init__(self, audio_loader):
        # Array results from each part
        self.corr_matrix_ary = []
        self.peak_sec_ary = []
        self.max_corr_ary = []

        # Map audio info to internal variables
        self.__audio_matrix = audio_loader.full_matrix.audio_matrix
        self.__sample_rate = audio_loader.full_matrix.sample_rate
        self.__audio_duration = audio_loader.full_matrix.audio_duration
        self.__audio_fragment_matrix = audio_loader.frag_matrix.audio_matrix

        # summary results
        self.exact_second = 0
        self.max_correlation = 0

    def find_segment(self, num_parts = 4):
        try:
            part_length = len(self.__audio_matrix) // num_parts
            #TODO - test whether there are performance improvements when processing matrix in parts
            #TODO - if there are performance gains, are there discontinuities in the correlate matrix at the boundaries?
            #TODO - if no performance gains, just process as single matrix and remove ENV variable
            
            for part_number in range(1, num_parts + 1):
                correlate_data = self._correlate(part_length=part_length, part_number=part_number)
                if correlate_data['error']: return correlate_data

            max_correlation_index = self.max_corr_ary.index(max(self.max_corr_ary))
            relative_peak_sec = self.peak_sec_ary[max_correlation_index]
            
            #TODO - stitch together all correlate sub-matrices and trim to full_audio length
            self.exact_second = (self.__audio_duration * max_correlation_index / num_parts) + relative_peak_sec
            self.max_correlation = self.max_corr_ary[max_correlation_index]
            #TODO - determine whether we ACTUALLY found the fragment (minimum correlation threshold?)

            return {"error": False,
                    "message": 'All correlations completed successfully'
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
            #TODO - how to prevent from processing part that is shorter than fragment duration?
            #TODO - what happens when we try to access array index out of bounds?
            audio_matrix_part = self.__audio_matrix[start:end]

            correlation = signal.correlate(audio_matrix_part, self.__audio_fragment_matrix, mode='valid', method='fft')

            peak = np.argmax(correlation)
            peak_second = peak / self.__sample_rate
            max_correlation = np.max(correlation)

            # Append part data to arrays
            self.corr_matrix_ary.append(correlation)
            self.peak_sec_ary.append(peak_second)
            self.max_corr_ary.append(max_correlation)

            return {
                "error": False,
                "message": 'This correlation completed successfully'
            }
        except Exception as error:
            return {
                "error": True,
                "message": f'Error in correlation: {str(error)}',
            }