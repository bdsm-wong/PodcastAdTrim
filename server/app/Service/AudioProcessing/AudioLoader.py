from ...Utils import AudioFileManager
import librosa
import logging

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)

class AudioLoader:
    def __init__(self, movie_audio_filename=None, sound_fragment_filename=None, custom_path=False):
        self.__movie_audio_filename = movie_audio_filename
        self.__sound_fragment_filename = sound_fragment_filename
        self.__custom_path = custom_path
        self.full_matrix = AudioFileManager()
        self.frag_matrix = AudioFileManager()

    def load_audio_data(self):
        # Load/generate matrix for full audio
        if self.__movie_audio_filename.endswith(".npz"):
            # Matrix already exists in storage.  Load it
            load_full_data = self.full_matrix.load_audio_matrix(
                file_name=self.__movie_audio_filename,
                custom_path=self.__custom_path)
        else:
            # Matrix doesn't yet exist.  Generate but don't save
            load_full_data = self.full_matrix.generate_temp_matrix(
                file_name=self.__movie_audio_filename,
                custom_path=self.__custom_path)

        if load_full_data['error']: return load_full_data

        # Load/generate matrix for audio fragment
        if self.__sound_fragment_filename.endswith(".npz"):
            # Matrix already exists in storage.  Load it
            load_frag_data = self.frag_matrix.load_audio_matrix(
                file_name=self.__sound_fragment_filename,
                custom_path=self.__custom_path)

            # Sample rate must match for correlation to work correctly
            if self.full_matrix.sample_rate != self.frag_matrix.sample_rate:
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
            load_frag_data = self.full_matrix.generate_temp_matrix(
                file_name=self.__movie_audio_filename,
                custom_path=self.__custom_path)

        return load_frag_data