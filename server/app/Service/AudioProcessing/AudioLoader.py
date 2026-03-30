from ...Utils import AudioFileManager
import librosa

class AudioLoader:
    def __init__(self, movie_audio_filename=None, sound_fragment_filename=None, logger=None):
        self.__movie_audio_filename = movie_audio_filename
        self.__sound_fragment_filename = sound_fragment_filename
        self.__logger = logger
        self.full_matrix = AudioFileManager(logger=logger)
        self.frag_matrix = AudioFileManager(logger=logger)

        # Flag indicating both matrices were already present in storage
        self.both_stored = True

    def load_audio_data(self):
        # Load/generate matrix for full audio
        if self.__movie_audio_filename.endswith(".npz"):
            # Matrix already exists in storage.  Load it
            load_full_data = self.full_matrix.load_audio_matrix(file_name=self.__movie_audio_filename)
        else:
            # Matrix doesn't yet exist.  Generate but don't save
            load_full_data = self.full_matrix.generate_temp_matrix(file_name=self.__movie_audio_filename)
            self.both_stored = False

        if load_full_data['error']: return load_full_data

        # Load/generate matrix for audio fragment
        if self.__sound_fragment_filename.endswith(".npz"):
            # Matrix already exists in storage.  Load it
            load_frag_data = self.frag_matrix.load_audio_matrix(file_name=self.__sound_fragment_filename)

            if load_frag_data['error']: return load_frag_data

            # Sample rate must match for correlation to work correctly
            elif self.full_matrix.sample_rate != self.frag_matrix.sample_rate:
                return {
                    "error": True,
                    "message": f'Full matrix sample rate ( \
                        {str(self.full_matrix.sample_rate)} Hz) \
                        must be equal to fragment matrix sample rate ( \
                        {str(self.frag_matrix.sample_rate)} Hz)'
                }
        else:
            # Since frag matrix doesn't yet exist, force it to use same sample rate as full
            self.frag_matrix.sample_rate = self.full_matrix.sample_rate

            # Matrix doesn't yet exist.  Generate but don't save
            load_frag_data = self.frag_matrix.generate_temp_matrix(file_name=self.__sound_fragment_filename)
            self.both_stored = False

            if load_frag_data['error']: return load_frag_data

        return load_frag_data