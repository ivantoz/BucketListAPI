from BucketListAPI.model import db
from BucketListAPI.model import User
from flask import abort


def create_user(data):
    username = data.get('username')
    password = data.get('password')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    if User.query.filter_by(username=username).all() is not None:
        abort(400, {'error': {'message': 'Username not available'}})
    user = User(username=username, first_name=first_name, last_name=last_name)
    user.hash_password(password)
    db.session.add(user)
    db.session.commit()
