# Imports
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

#------------------------------ Flask Setup ------------------------

app = Flask(__name__)

app.config['SECRET_KEY'] = '4c673c0ef7953896bc739e5c6161b2ad'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///comunidade.db"

database = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'alert-info'
login_manager.login_message = 'Por favor, faça o login ou crie sua conta para acessar esse conteúdo!'

# Run
from comunidadeimpressionadora import routes