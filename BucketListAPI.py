from flask import Flask
from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
# app.config.from_envvar('SECRET_KEY', silent=True)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
# app.config.from_envvar('SQLALCHEMY_DATABASE_URI', silent=True)
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'

toolbar = DebugToolbarExtension(app)

if __name__ == '__main__':
    app.run()
