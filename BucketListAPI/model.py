import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import current_app
import jwt


db = SQLAlchemy()


class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    bucketlists = db.relationship('Bucketlist', backref='users',cascade="all, delete, "
                                                                        "delete-orphan",
                                  lazy="joined")

    def __init__(self, email, password, admin=False):
        from BucketListAPI.app import bcrypt
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode()
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def encode_auth_token(self, user_id):
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=3000),
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
        except Exception as e:
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


class BlacklistToken(db.Model):
    """
    Token Model for storing JWT tokens
    """
    __tablename__ = 'blacklist_tokens'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, nullable=False)

    def __init__(self, token):
        self.token = token
        self.blacklisted_on = datetime.datetime.now()

    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def check_blacklist(auth_token):
        # check whether auth token has been blacklisted
        res = BlacklistToken.query.filter_by(token=str(auth_token)).first()
        if res:
            return True
        else:
            return False


class Bucketlist(db.Model):
    __tablename__ = 'bucketlist'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    items = db.relationship('BucketListItem', backref='bucketlist',
                            cascade='all, delete, delete-orphan', single_parent=True,
                            lazy='dynamic')
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '< id: {} name: {} date_created: {} date_modified: {} created_by: {}'.format(
            self.id, self.name, self.date_created, self.date_modified, self.created_by
        )


class BucketListItem(db.Model):
    __tablename__ = 'bucketlistitem'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey('bucketlist.id', ondelete='CASCADE'),
                              nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    done = db.Column(db.Boolean)

    def __init__(self, name, bucketlist_id, done=False):
        self.name = name
        self.bucketlist_id = bucketlist_id
        self.done = done

    def __repr__(self):
        return '<id: {} name: {} bucketlist_id: {} date_created: {} date_modified: {} done: {}'.format(
            self.id, self.name, self.bucketlist_id, self.date_created, self.date_modified, self.done
        )







