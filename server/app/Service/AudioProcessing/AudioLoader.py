from ...Utils import AudioFileManager
import librosa
import logging

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)

class AudioLoader:
    def __init__(self, movie_audio_filename=None, sound_fragment_filename=None, custom_path=False):
        self.__movie_audio_filename = movie_audio_filename
        self.__sound_fragment_filename = sound_fragment_filename
        self.__custom_path = custom_path
        self.audio_matrix = None
        self.sample_rate = None
        self.audio_duration = None
        self.audio_fragment_matrix = None
        self.fragment_audio_duration = None

    def load_audio_data(self):
        if self.__movie_audio_filename.endswith(".npz"):
            load_audio_data = self._load_npz_audio_data()
        elif self.__movie_audio_filename and self.__sound_fragment_filename:
            load_audio_data = self._load_normal_audio_data()
        else:
            return {
                "error": True,
                "message": "Invalid combination of audio files provided.",
            }
        
        if load_audio_data['error']: return load_audio_data

        try:
            self.audio_fragment_matrix, _ = librosa.load(path=self.__sound_fragment_filename, sr=self.sample_rate)
            self.fragment_audio_duration = librosa.get_duration(path=self.__sound_fragment_filename)

            return {"error": False, "message": "Data loading successful"}
        except Exception as error:
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error loading fragment audio: {str(error)}',
            }

    def _load_npz_audio_data(self):
        try:
            audio_data = AudioFileManager.load_audio_matrix(self.__movie_audio_filename, self.__custom_path)
            if audio_data['error']:
                return audio_data

            self.audio_matrix = audio_data['message']['audio_matrix']
            self.sample_rate = audio_data['message']['sample_rate']
            self.audio_duration = audio_data['message']['audio_duration']
            
            return {"error": False, "message": "Data loading successful"}
        except Exception as error:
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error loading audio matrix file: {str(error)}',
            }

    def _load_normal_audio_data(self):
        try:
            self.audio_matrix, self.sample_rate = librosa.load(path=self.__movie_audio_filename, sr=None)
            self.audio_duration = librosa.get_duration(path=self.__movie_audio_filename, sr=self.sample_rate)

            return {"error": False, "message": "Data loading successful"}
        except Exception as error:
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error loading original audio: {str(error)}',
            }