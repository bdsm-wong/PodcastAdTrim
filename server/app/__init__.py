from flask import Flask
import logging

#TODO - read in log level from ENV file
logging.basicConfig(filename='audio_detection_service.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s : %(message)s')

app = Flask(__name__)

from .Service import AudioProcessor
from .Routes import api