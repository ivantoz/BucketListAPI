from flask import Flask
# from flask_debugtoolbar import DebugToolbarExtension
import os
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

from model import Result

@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/<name>')
def hello_name(name):
    return "Hello {}!".format(name)


# toolbar = DebugToolbarExtension(app)

print(os.environ['APP_SETTINGS'])

if __name__ == '__main__':
    app.run()
