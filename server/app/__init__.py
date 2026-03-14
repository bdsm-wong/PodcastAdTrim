from flask import Flask

app = Flask(__name__)

from .Service import AudioProcessor
from .Routes import api