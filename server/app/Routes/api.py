from flask import request
from .. import app
from ..Controllers import AudioDetectionController, AudioStorageController
from ..Middleware import AudioDetectionMiddleware, AudioStorageMiddleware, OptionalInputMiddleware
from ..Utils import ResponseHttp

@app.before_request
def before_request():
    endpoint_middlewares = {
        'audio_detection': (OptionalInputMiddleware, AudioDetectionMiddleware),
        'audio_storage': (AudioStorageMiddleware,)
    }
    endpoint = request.endpoint
    middlewares = endpoint_middlewares.get(endpoint, ())

    for middleware in middlewares:
        result = middleware.invokable(request=request)
        if result['error']:
            return ResponseHttp.error_message(message=result['message'], status_code=400)
    
@app.route('/audio-detection', methods=['POST'])
def audio_detection():
    return AudioDetectionController.invokable(request=request,logger=app.logger)

@app.route('/audio-storage', methods=['POST'])
def audio_storage():
    return AudioStorageController.invokable(request=request,logger=app.logger)

@app.route('/health')
def health():
    return "Healthy!"