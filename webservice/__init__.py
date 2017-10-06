from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object('webservice.config.Development')

db = SQLAlchemy(app)

from webservice.handlers import *
from webservice.models import *