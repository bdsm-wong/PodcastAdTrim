from flask import Flask

app = Flask(__name__)

from server.app.Service import AudioProcessor
from server.app.Routes import api