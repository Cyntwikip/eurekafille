from flask import Flask

app = Flask(__name__)

from app import routes
from lib import eurekabot
from lib import departures
