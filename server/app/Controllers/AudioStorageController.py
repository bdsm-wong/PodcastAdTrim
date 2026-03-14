from flask import jsonify
from server.app.Utils import AudioFileManager, ResponseHttp
import tempfile
import io

class AudioStorageController:
    """
        {
            name_full_audio: string (name of how the file will be saved in the storage directory),
            full_audio: audio_file
        }
    """
    @staticmethod
    def invokable(request):
        try:
            data = request.form.to_dict()
            name_full_audio = f"{data.get('name_full_audio')}.npz"

            file_full_audio = request.files['full_audio']
            full_audio_data = io.BytesIO(file_full_audio.read())
            with tempfile.NamedTemporaryFile(delete=False) as temp_full_audio_file:
                    temp_full_audio_file.write(full_audio_data.read())
                    temp_full_audio_file_name = temp_full_audio_file.name

            audio_file_manager = AudioFileManager.save_audio_matrix(audio_path=temp_full_audio_file_name, file_name=name_full_audio)

            if(audio_file_manager['error']): return ResponseHttp.error_message(message=audio_file_manager['message'],status_code=500)
            return ResponseHttp.successful_message([audio_file_manager['message']])
        except Exception as e:
            return ResponseHttp.error_message(message=f'AudioStorageControler => {e} ', status_code=500)