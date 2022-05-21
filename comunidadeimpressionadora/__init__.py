# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt

#------------------------------ Flask Setup ------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = '4c673c0ef7953896bc739e5c6161b2ad'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///comunidade.db'

#------------------------------ Database ------------------------

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)

from comunidadeimpressionadora import routes