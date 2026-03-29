from flask import Flask
from dotenv import load_dotenv
import os
import logging

load_dotenv()
logLevelStr = os.getenv('LOG_LEVEL', default='ERROR').upper()
logging.basicConfig(filename='audio_detection_service.log', level=logLevelStr, format=f'%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)

from .Service import AudioProcessor
from .Routes import api