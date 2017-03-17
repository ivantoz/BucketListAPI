import datetime
from BucketListAPI.app import db


class Bucketlist(db.Model):
    __tablename__ = 'BucketListAPI'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(80))
    date_created = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    date_modified = db.Column(db.DateTime, onupdate=datetime.datetime.utcnow)
    created_by = db.Column(db.Integer) #db.ForeignKey(User.id)

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




