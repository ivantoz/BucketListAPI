import logging

from flask import request
from flask_restplus import Resource

from BucketListAPI.api.auth.business import create_user
from BucketListAPI.api.auth.serializers import new_user
from BucketListAPI.api.restplus import api
from BucketListAPI.model import Bucketlist, BucketListItem

log = logging.getLogger(__name__)

ns = api.namespace('auth/register', description='Operations related to User registration')


@ns.route('/')
class UserCollection(Resource):

    @api.response(201, 'User successfully created.')
    @api.expect(new_user)
    def post(self):
        """
        Create a new User.
        """
        data = request.json
        create_user(data)
        return None, 201
