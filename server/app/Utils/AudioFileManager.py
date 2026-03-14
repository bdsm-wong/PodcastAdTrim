from dotenv import load_dotenv
import numpy as np
import logging
import librosa
import os

logging.basicConfig(filename='audio_detection_service.log', level=logging.ERROR)

load_dotenv()

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
    @staticmethod
    def save_audio_matrix(audio_path, file_name, custom_path=False):
        storage_path = os.getenv("STORAGE_PATH") + file_name if not custom_path else file_name
        try:
            audio_matrix, sample_rate = librosa.load(path=audio_path, sr=None)
            audio_duration = librosa.get_duration(path=audio_path, sr=sample_rate)
            
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
    def load_audio_matrix(file_name, custom_path=False):
        storage_path = os.getenv("STORAGE_PATH") + file_name if not custom_path else file_name
        try:
            data = np.load(storage_path)
            return {"error": False,
                    "message": {
                        "audio_matrix": data["audio_matrix"],
                        "sample_rate": data["sample_rate"],
                        "audio_duration": data["audio_duration"]
                    }}
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