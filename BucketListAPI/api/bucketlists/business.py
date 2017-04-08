from BucketListAPI.model import db
from BucketListAPI.model import Bucketlist, BucketListItem
from flask import abort
from flask_sqlalchemy import BaseQuery


def create_bucketlist_item(id, data):
    name = data.get('name')
    done = data.get('done')
    bucketlist_id = id
    bucketlist_item = BucketListItem(name, bucketlist_id, done=done)
    if Bucketlist.query.filter_by(id=id).first() is not None:
        db.session.add(bucketlist_item)
        db.session.commit()
        responseObject = {
            'status': 'success',
            'message': 'Bucketlist item successfully created.'
        }
        return responseObject
    else:
        abort(404, {'error': {'message': 'Bucketlist not found'}})


def update_item(id, item_id, data):
    item = BucketListItem.query.get_or_404(item_id)
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    item.name = name
    item.done = data.get('done')
    db.session.add(item)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Bucketlist item successfully updated.'
    }
    return responseObject


def delete_item(item_id):
    item = BucketListItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Item successfully deleted.'
    }
    return responseObject


def create_bucketlist(data):
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    created_by = data.get('created_by')
    bucketlist = Bucketlist(name, created_by)

    db.session.add(bucketlist)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Bucketlist successfully created.'
    }
    return responseObject


def update_bucketlist(bucketlist_id, data):
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    bucketlist = Bucketlist.query.get_or_404(bucketlist_id)
    bucketlist.name = name
    db.session.add(bucketlist)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Bucketlist item successfully updated.'
    }
    return responseObject


def delete_bucketlist(b_id):
    bucketlist = Bucketlist.query.get_or_404(b_id)
    db.session.delete(bucketlist)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'BucketList item successfully deleted.'
    }
    return responseObject



