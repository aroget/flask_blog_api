from flask import Flask
from flask.ext.cache import Cache
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

cache = Cache(app,config={'CACHE_TYPE': 'simple'})
app.config.from_object('webservice.config.Development')

db = SQLAlchemy(app)

from webservice.handlers import *
from webservice.models import *