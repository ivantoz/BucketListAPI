import logging.config
import os

from flask import Flask, Blueprint

from BucketListAPI.api.bucketlists.endpoints.bucketlist import ns as bucketlist_namespace
from BucketListAPI.api.auth.endpoints.register import ns as auth_new_user_namespace
from BucketListAPI.api.restplus import api
from BucketListAPI.model import db


app = Flask(__name__)
logging.config.fileConfig('logging.conf')
log = logging.getLogger(__name__)


def configure_app(flask_app):
    flask_app.config.from_object(os.environ['APP_SETTINGS'])


def initialize_app(flask_app):
    configure_app(flask_app)

    blueprint = Blueprint('api', __name__, url_prefix='/api/v1')
    api.init_app(blueprint)
    api.add_namespace(auth_new_user_namespace)
    api.add_namespace(bucketlist_namespace)
    flask_app.register_blueprint(blueprint)
    db.init_app(flask_app)


def main():
    initialize_app(app)
    log.info('>>>>> Starting development server at http://{}/api/v1/ <<<<<'.format(
        app.config['FLASK_SERVER_NAME']))
    app.run(debug=app.config['DEBUG'])


if __name__ == '__main__':
    main()
