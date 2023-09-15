#initialize the app
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__,instance_relative_config=True)

#load the config
app.config.from_pyfile('config.py',silent=False)

#instantiaiting an object of sqlalchemy
db=SQLAlchemy(app)

#load the routes
from rubygymapp import clientroutes