from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
import jinja2

from app import settings

pcb = Flask(__name__)
pcb.config.from_object(settings)

db = SQLAlchemy(pcb)

from views import *
