from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy

from app import settings

pcb = Flask(__name__)
pcb.config.from_object(settings)
db = SQLAlchemy(pcb)

from views import *
