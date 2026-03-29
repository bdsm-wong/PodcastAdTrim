from flask import jsonify
from ..Utils import AudioFileManager, ResponseHttp
import tempfile
import io
import time

class AudioStorageController:
    """
        {
            type_audio: string (file type - 'full' or 'frag'),
            name_audio: string (name of how the file will be saved in the storage directory),
            file_audio: audio_file
        }
    """
    @staticmethod
    def invokable(request,logger):
        try:
            storage_start_time = time.time()
            data = request.form.to_dict()
            storage_path = f"{data.get('type_audio')}/{data.get('name_audio')}.npz"

            file_audio = request.files['file_audio']
            audio_data = io.BytesIO(file_audio.read())
            with tempfile.NamedTemporaryFile(delete=False) as temp_audio_file:
                    temp_audio_file.write(audio_data.read())
                    temp_audio_file_name = temp_audio_file.name

            audio_file_manager = AudioFileManager.save_audio_matrix(
                audio_path=temp_audio_file_name,
                file_name=storage_path,
                logger=logger)

            if(audio_file_manager['error']): return ResponseHttp.error_message(message=audio_file_manager['message'],status_code=500)
            storage_end_time = time.time()
            storage_elapsed_time = storage_end_time - storage_start_time

            return ResponseHttp.successful_message(f"{audio_file_manager['message']}.  Completed in {str(storage_elapsed_time)} seconds.")
        except Exception as e:
            return ResponseHttp.error_message(message=f'AudioStorageControler => {e} ', status_code=500)