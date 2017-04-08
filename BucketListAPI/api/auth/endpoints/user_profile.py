import logging
from flask import request
from flask_restplus import Resource
from BucketListAPI.api.auth.serializers import login
from BucketListAPI.api.restplus import api
from BucketListAPI.api.auth.business import login_user


log = logging.getLogger(__name__)

ns = api.namespace('auth/login', description='Operations related to User login')


@ns.route('/')
class UserLogin(Resource):
    @api.response(200, 'User authorized.')
    @api.expect(login)
    def post(self):
        """
        Verify User.
        """
        data = request.json
        return login_user(data)





