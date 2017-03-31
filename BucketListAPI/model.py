import datetime
from flask_sqlalchemy import SQLAlchemy

from BucketList.app import app

from passlib.apps import custom_app_context as pwd_context
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)



db = SQLAlchemy()


class Bucketlist(db.Model):
    __tablename__ = 'BucketList'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey(User.id))

    def __init__(self, name, created_by):
        self.name = name
        self.created_by = created_by

    def __repr__(self):
        return '< id: {} name: {} date_created: {} date_modified: {} created_by: {}'.format(
            self.id, self.name, self.date_created, self.date_modified, self.created_by
        )


class BucketListItems(db.Model):
    __tablename__ = 'bucketlistitems'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    bucketlist_id = db.Column(db.Integer, db.ForeignKey(Bucketlist.id))
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


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(32), index=True)
    password_hash = db.Column(db.String(64))

    def hash_password(self, password):
        self.password_hash = pwd_context.encrypt(password)

    def verify_password(self, password):
        return pwd_context.verify(password, self.password_hash)

    def generate_auth_token(self, expiration=600):
        s = Serializer(app.config['SECRET_KEY'], expires_in=expiration)
        return s.dumps({'id': self.id})

    @staticmethod
    def verify_auth_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except SignatureExpired:
            return None    # valid token, but expired
        except BadSignature:
            return None    # invalid token
        user = User.query.get(data['id'])
        return user


