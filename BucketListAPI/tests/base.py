from flask_testing import TestCase

from flask import current_app
from BucketListAPI.app import app, initialize_app
from BucketListAPI.model import db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):

        app.config.from_object('BucketListAPI.config.TestingConfig')
        initialize_app(app)
        # db.init_app(app)
        return app

    def setUp(self):
        with app.app_context():
            db.create_all()
            db.session.commit()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()
