import numpy as np
import librosa
import os

class AudioFileManager:
    """
    Manages the conversion of an audio file to a matrix and the saving/loading of the matrix to/from a binary file.

    Args:
        audio_path (str): Path to the audio file to be processed.
        file_name (str): Name of the file to save (e.g., 'example.npz').

    Returns:
        dict: A dictionary with two keys:
            - 'error' (bool): True if an error occurred during the operation, False otherwise.
            - 'message' (str): A message indicating the result of the operation.
    """
    def __init__(self,logger):
        self.audio_matrix = None
        self.sample_rate = None
        self.audio_duration = None
        self.logger = logger

    @staticmethod
    def save_audio_matrix(audio_path, file_name, logger):
        storage_path = "./storage/" + file_name
        try:
            audio_matrix, sample_rate = librosa.load(path=audio_path, sr=None)
            audio_duration = librosa.get_duration(path=audio_path, sr=sample_rate)

            # Create any missing subdirectories
            # Remove "fileName.npz" so we don't create that as a directory
            last_slash = storage_path.rfind("/")
            storage_dirs = storage_path[:last_slash]
            os.makedirs(storage_dirs, exist_ok=True)

            np.savez(storage_path,
                     audio_matrix=audio_matrix,
                     sample_rate=sample_rate,
                     audio_duration=audio_duration
                     )
            return {"error": False, "message": "Audio matrix saved successfully"}
        except Exception as error:
            logger.error(str(error))
            return {
                "error": True,
                "message": f'Error saving audio matrix: {str(error)}',
            }

    @staticmethod
    def save_correlate_matrix(movie_audio_filename, sound_fragment_filename, audio_locator, logger):
        # Save result matrix from correlate process
        # Location: ./storage/corr/[full]/[frag].npz

        full_name = movie_audio_filename.replace("full/", "").replace(".npz", "")
        frag_name = sound_fragment_filename.replace("frag/", "").replace(".npz", "")
        storage_dir = "./storage/corr/" + full_name
        try:
            os.makedirs(storage_dir, exist_ok=True)
            storage_path = storage_dir + "/" + frag_name

            np.savez(storage_path,
                     corr_matrix=audio_locator.correlation_matrix,
                     exact_second=audio_locator.exact_second
                     )

            return {"error": False, "message": "Correlation matrix saved successfully"}
        except Exception as error:
            logger.error(str(error))
            return {
                "error": True,
                "message": f'Error saving correlation matrix: {str(error)}',
            }

    def load_audio_matrix(self, file_name):
        storage_path = "./storage/" + file_name
        try:
            data = np.load(storage_path)
            self.audio_matrix = data["audio_matrix"]
            self.sample_rate = data["sample_rate"]
            self.audio_duration = data["audio_duration"]
            return {
                "error": False,
                "message": 'Audio matrix loaded successfully'
            }
        except FileNotFoundError:
            return {
                "error": True,
                "message": 'The file does not exist',
            }
        except Exception as error:
            return {
                "error": True,
                "message": f'Error loading audio matrix: {str(error)}',
            }

    def generate_temp_matrix(self, file_name):
        try:
            # Pass sample_rate in AND out in case it changes between init and method call
            self.audio_matrix, self.sample_rate = librosa.load(path=file_name, sr=self.sample_rate)
            self.audio_duration = librosa.get_duration(path=file_name, sr=self.sample_rate)
            return {
                "error": False,
                "message": 'Audio matrix generated successfully'
            }
        except Exception as error:
            self.logger.error(str(error))
            return {
                "error": True,
                "message": f'Error generating audio matrix: {str(error)}',
            }