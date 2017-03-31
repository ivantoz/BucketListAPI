from flask_restplus import fields
from BucketListAPI.api.restplus import api


new_user = api.model('User', {
    'username': fields.String(required=True, description='unique Username'),
    'password': fields.String(required=True, description='User password'),
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name')
})
