class AudioFormat:
    @staticmethod
    def validate_extension(filename):
        # Check if the file extension is in the list of allowed audio formats
        allowed_formats = ['.mp3', '.wav', '.m4a', '.ogg']
        return any(filename.lower().endswith(format) for format in allowed_formats)