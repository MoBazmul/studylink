#!/usr/bin/python3
"""
Initialization of Flask application and extensions.

Imports necessary modules and initializes Flask application along with SQLAlchemy,
Flask-Bcrypt, Flask-Login, Flask-Migrate, dotenv, and Flask-Moment extensions.
"""

import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from dotenv import load_dotenv
from flask_moment import Moment
from flask_mail import Mail

# Initialize Flask application
app = Flask(__name__)
load_dotenv()

# Configure application
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy, Flask-Bcrypt, Flask-Login, Flask-Migrate, and Flask-Moment extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt()
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
moment = Moment(app)
mail = Mail(app)

# Import routes from studylink module
from studylink import routes
