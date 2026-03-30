from scipy import signal
import numpy as np

class AudioLocator:

    def __init__(self, audio_loader, logger):
        # Combined array with correlation results from each part
        self.corr_matrix_ary = []

        self.__logger = logger

        # Map audio info to internal variables
        self.__audio_matrix = audio_loader.full_matrix.audio_matrix
        self.__sample_rate = audio_loader.full_matrix.sample_rate
        self.__audio_duration = audio_loader.full_matrix.audio_duration
        self.__audio_fragment_matrix = audio_loader.frag_matrix.audio_matrix

        # summary results
        self.exact_second = 0
        self.max_correlation = 0

    def find_segment(self, max_partition_size=5300000):
        try:
            full_matrix_len = len(self.__audio_matrix)
            full_matrix_max_idx = full_matrix_len - 1
            frag_matrix_len = len(self.__audio_fragment_matrix)

            self.__logger.info(f'full_matrix_len: {str(full_matrix_len)}, frag_matrix_len: {str(frag_matrix_len)}')

            if frag_matrix_len > full_matrix_len:
                return {"error": True,
                        "message": f'Fragment matrix length ({str(frag_matrix_len)}) exceeds full matrix length ({str(full_matrix_len)}).'
                        }

            if frag_matrix_len > max_partition_size:
                return {"error": True,
                        "message": f'Fragment matrix length ({str(frag_matrix_len)}) exceeds max partition size ({str(max_partition_size)}).'
                        }

            start = 0
            end = 0
            while end < full_matrix_max_idx:
                #set bounds of the correlation partition
                if start + max_partition_size > full_matrix_max_idx:
                    end = full_matrix_max_idx
                else:
                    end = start + max_partition_size - 1

                correlate_data = self._correlate(start=start, end=end)
                if correlate_data['error']: return correlate_data

                # Shift back start of next partition to allow "overscanning" during correlation
                # This is required to eliminate discontinuities at partition boundaries
                start = end - frag_matrix_len

            #TODO - watch for "off by one" errors while traversing arrays
            #TODO - determine whether we ACTUALLY found the fragment (minimum correlation threshold?)

            return {"error": False,
                    "message": 'All correlations completed successfully'
                    }
        except Exception as error:
            return {
                "error": True,
                "message": f'Error finding segment: {str(error)}',
            }

    def _correlate(self, start, end):
        try:
            audio_matrix_part = self.__audio_matrix[start:end]

            correlation = signal.correlate(audio_matrix_part, self.__audio_fragment_matrix, mode='valid', method='fft')

            # Compare local correlation max to overall max and compute/update timestamp as needed
            this_max_corr = np.max(correlation)
            if this_max_corr > self.max_correlation:
                peak_idx = np.argmax(correlation) + start
                self.exact_second = peak_idx / self.__sample_rate

            # Append part data to arrays
            #self.corr_matrix_ary = np.concatenate((self.corr_matrix_ary,correlation),axis=0)

            self.__logger.info(f'start: {str(start)}, end: {str(end)}, len(correlation): {str(len(correlation))}')

            return {
                "error": False,
                "message": 'This correlation completed successfully'
            }
        except Exception as error:
            return {
                "error": True,
                "message": f'Error in correlation: {str(error)}',
            }