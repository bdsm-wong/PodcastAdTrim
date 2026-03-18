import numpy as np
import logging
import librosa
import os

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)


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
    def __init__(self):
        self.audio_matrix = None
        self.sample_rate = None
        self.audio_duration = None

    @staticmethod
    def save_audio_matrix(audio_path, file_name, custom_path=False):
        storage_path = "./storage/" + file_name if not custom_path else file_name
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
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error saving audio matrix: {str(error)}',
            }

    @staticmethod
    def save_correlate_matrix():
        #TODO - save result matrix/matrices from correlate process
        # Location: ./storage/corr/[full]/[frag].npz
        pass

    def load_audio_matrix(self, file_name, custom_path=False):
        storage_path = "./storage/" + file_name if not custom_path else file_name
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
            logging.error(f'Error: {str(error)}')
            return {
                "error": True,
                "message": f'Error generating audio matrix: {str(error)}',
            }