class AudioFormat:
    @staticmethod
    def validate_extension(filename):
        # Check if the file extension is in the list of allowed audio formats
        allowed_formats = ['.mp3', '.wav', '.m4a', '.ogg']
        return any(filename.lower().endswith(format) for format in allowed_formats)

    @staticmethod
    def request_type(request,key):
        # determine key is a file or form
        if key in request.files:
            return "file"
        elif key in request.form:
            return "name"
        else:
            return None