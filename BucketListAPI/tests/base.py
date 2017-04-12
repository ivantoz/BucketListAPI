from flask_testing import TestCase
from flask_testing.utils import _make_test_response
from flask import Flask
from BucketListAPI.app import initialize_app
from BucketListAPI.model import db


class BaseTestCase(TestCase):
    """ Base Tests """

    def create_app(self):
        app = Flask(__name__)
        app.config.from_object('BucketListAPI.config.TestingConfig')
        initialize_app(app)
        return app

    def setUp(self):

        self.app = self.create_app()
        self._orig_response_class = self.app.response_class
        self.app.response_class = _make_test_response(self.app.response_class)
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()
        db.create_all()
        db.session.commit()

    def tearDown(self):
        if getattr(self, '_ctx', None) is not None:
            self._ctx.pop()
            del self._ctx
        if getattr(self, 'app', None) is not None:
            if getattr(self, '_orig_response_class', None) is not None:
                self.app.response_class = self._orig_response_class
            del self.app
        db.session.remove()
        db.drop_all()




