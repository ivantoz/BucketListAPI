import logging.config

from flask import Flask, Blueprint
import os
from BucketListAPI.api.restplus import api
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
logging.config.fileConfig('logging.cong')
log = logging.getLogger(__name__)

db = SQLAlchemy()


def configure_app(flask_app):
    flask_app.config.from_object(os.environ['APP_SETTINGS'])


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api')
    api.init_app(blueprint)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/ <<<<<'.format(
        app.config['SERVER_NAME']))
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    app.run()
