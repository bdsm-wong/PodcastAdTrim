from flask import Flask
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(filename='audio_detection_service.log', format=f'%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)

load_dotenv()
logLevelStr = os.getenv('LOG_LEVEL', default='ERROR').upper()

try:
    app.logger.setLevel(logLevelStr)
except ValueError:
    app.logger.setLevel(logging.ERROR)
    app.logger.ERROR(f"Invalid Log Level in .env file: {logLevelStr}.  ERROR used instead.")

from .Service import AudioProcessor
from .Routes import api