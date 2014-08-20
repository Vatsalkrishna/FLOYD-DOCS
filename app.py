import os

from flask import Flask, render_template, request, redirect, g  
from flask.ext.mongoengine import MongoEngine, MongoEngineSessionInterface
from flask.ext.login import LoginManager


app = Flask("dbmsApp")  #create and name the flask project
app.config['SECRET_KEY'] = '123456790'

# for database connections
app.config['MONGODB_SETTINGS'] = {'HOST':os.environ.get('MONGOLAB_URI'),'DB': 'FlaskLogin'}
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
app.debug = os.environ.get('DEBUG',False)


db = MongoEngine(app)  #connecting mongo engine with flask app
app.session_interface = MongoEngineSessionInterface(db)  #for sessins with mongoengine

login_manager = LoginManager()

login_manager.init_app(app)  #associate flask login manager with current app
