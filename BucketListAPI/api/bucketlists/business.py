from BucketListAPI.model import db
from BucketListAPI.model import Bucketlist, BucketListItem
from flask import abort


def create_bucketlist_item(id, data):
    name = data.get('name')
    done = data.get('done')
    bucketlist_id = id
    bucketlist_item = BucketListItem(name, bucketlist_id, done=done)
    if Bucketlist.query.filter_by(id=id).first() is not None:
        db.session.add(bucketlist_item)
        db.session.commit()
    else:
        abort(404, {'error': {'message': 'Bucketlist not found'}})


def update_item(id, item_id, data):
    item = BucketListItem.query.filter(id == item_id).one()
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    item.name = name
    item.done = data.get('done')
    bucketlist_id = data.get('bucketlist_id')
    item.bucketlist_id = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    db.session.add(item)
    db.session.commit()


def delete_item(item_id):
    try:
        item = BucketListItem.query.filter(BucketListItem.id == item_id).one()

        db.session.delete(item)
        db.session.commit()
    except Exception as e:
        abort(400, {'error': {'message': str(e)}})


def create_bucketlist(data):
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    created_by = data.get('created_by')
    bucketlist = Bucketlist(name, created_by)

    db.session.add(bucketlist)
    db.session.commit()


def update_bucketlist(bucketlist_id, data):
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    bucketlist.name = name
    db.session.add(bucketlist)
    db.session.commit()


def delete_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).all()
    db.session.delete(bucketlist)
    db.session.commit()
