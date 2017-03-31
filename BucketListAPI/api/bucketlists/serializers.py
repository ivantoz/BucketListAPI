from flask_restplus import fields
from BucketList.api.restplus import api

bucketlist_item = api.model('Bucketlist Item', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a bucketlist item'),
    'name': fields.String(required=True, description='Bucketlist item name'),
    'date_created': fields.DateTime,
    'bucketlist_id': fields.Integer(attribute='bucketlist.id'),
    'done': fields.Boolean(required=True),
})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

page_of_bucketlist_item = api.inherit('Page of bucketlis item', pagination, {
    'items': fields.List(fields.Nested(bucketlist_item))
})

bucketlist = api.model('Bucketlist', {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Bucketlist'),
    'name': fields.String(required=True, description='Bucketlist name'),
    'date_created': fields.DateTime,
    'created_by': fields.Integer(required=True)
})

bucketlist_with_items = api.inherit('Bucketlist with items', bucketlist, {
    'items': fields.List(fields.Nested(bucketlist_item))
})
