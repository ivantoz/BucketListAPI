from BucketListAPI.model import db
from BucketListAPI.model import Bucketlist, BucketListItem
from flask import abort, current_app, _app_ctx_stack


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
    name = data.get('name')
    if not name.strip():
        abort(400, {"errors": {"name": "'name' is a required property"},
                    "message": "Input payload validation failed"})
    with current_app.app_context():
        user_data = _app_ctx_stack.user_data
        created_by = user_data['user_id']
    try:
        item = Bucketlist.query.filter_by(
                    created_by=created_by, id=id).first().items.filter_by(id=item_id).first_or_404()

        item.name = name
        item.done = data.get('done')
        db.session.add(item)
        db.session.commit()
        responseObject = {
            'status': 'success',
            'message': 'Bucketlist item successfully updated.'
        }
        return responseObject
    except Exception:
        abort(400)


def delete_item(id, item_id):
    with current_app.app_context():
        user_data = _app_ctx_stack.user_data
        created_by = user_data['user_id']
    item = Bucketlist.query.filter_by(
        created_by=created_by, id=id).first().items.filter_by(id=item_id)
    if not item.count():
        abort(403)
    db.session.delete(item.first_or_404())
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
    with current_app.app_context():
        user_data = _app_ctx_stack.user_data
        created_by = user_data['user_id']
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
    with current_app.app_context():
        user_data = _app_ctx_stack.user_data
        created_by = user_data['user_id']
    bucketlist = Bucketlist.query.filter_by(created_by=created_by, id=bucketlist_id).first_or_404()
    bucketlist.name = name
    db.session.add(bucketlist)
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'Bucketlist item successfully updated.'
    }
    return responseObject


def delete_bucketlist(b_id):
    with current_app.app_context():
        user_data = _app_ctx_stack.user_data
        created_by = user_data['user_id']
    bucketlist = Bucketlist.query.filter_by(created_by=created_by, id=b_id)
    if not bucketlist.count():
        abort(403)
    db.session.delete(bucketlist.first_or_404())
    db.session.commit()
    responseObject = {
        'status': 'success',
        'message': 'BucketList item successfully deleted.'
    }
    return responseObject



