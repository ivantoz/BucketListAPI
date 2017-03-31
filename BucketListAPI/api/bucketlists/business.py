from BucketList.model import db
from BucketList.model import Bucketlist, BucketListItems


def create_bucketlist_item(data):
    name = data.get('name')
    done = data.get('done')
    bucketlist_id = data.get('bucketlist_id')
    bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    bucketlist_item = BucketListItems(name, bucketlist, done=done)
    db.session.add(bucketlist_item)
    db.session.commit()


def update_item(item_id, data):
    item = BucketListItems.query.filter(BucketListItems.id == item_id).one()
    item.name = data.get('name')
    item.done = data.get('done')
    bucketlist_id = data.get('bucketlist_id')
    item.bucketlist_id = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    db.session.add(item)
    db.session.commit()


def delete_item(item_id):
    item = BucketListItems.query.filter(BucketListItems.id == item_id).one()
    db.session.delete(item)
    db.session.commit()


def create_bucketlist(data):
    name = data.get('name')
    created_by = data.get('created_by')

    bucketlist = Bucketlist(name)
    bucketlist.created_by = created_by

    db.session.add(bucketlist)
    db.session.commit()


def update_bucketlist(bucketlist_id, data):
    bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    bucketlist.name = data.get('name')
    db.session.add(bucketlist)
    db.session.commit()


def delete_bucketlist(bucketlist_id):
    bucketlist = Bucketlist.query.filter(Bucketlist.id == bucketlist_id).one()
    db.session.delete(bucketlist)
    db.session.commit()
