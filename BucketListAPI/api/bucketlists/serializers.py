from flask_restplus import fields
from BucketListAPI.api.restplus import api

bucketlist_item = api.model('Bucketlist Item', {
    'name': fields.String(required=True, description='Bucketlist item name', example='Climb to  '
                                                                                     'the Peak of Mt. Kenya'),
    'done': fields.Boolean(required=True, example=True)
})

bucketlist_item_output = api.inherit('Bucketlist item output', bucketlist_item, {
    'id': fields.Integer(readOnly=True, description='The unique identifier of a Bucketlist item'),
    'date_modified': fields.DateTime(description='date modified'),
    'date_created': fields.DateTime,

})

pagination = api.model('A page of results', {
    'page': fields.Integer(description='Number of this page of results'),
    'pages': fields.Integer(description='Total number of pages of results'),
    'per_page': fields.Integer(description='Number of items per page of results'),
    'total': fields.Integer(description='Total number of results'),
})

bucketlist_input = api.model('Bucketlist', {
    'name': fields.String(required=True, description='Bucketlist name', example='Climb Mountain')

})

bucketlist = api.model('Bucketlist', {
    'id': fields.Integer(readOnly=True, nullable=False, description='The unique identifier of a  '
                                                                    'Bucketlist'),
    'name': fields.String(required=True, description='Bucketlist name', example='Climb Mountain'),
    'date_created': fields.DateTime,
    'date_modified': fields.DateTime,
    'created_by': fields.Integer(required=True, example=1)

})

bucketlist_with_items = api.inherit('Bucketlist with items', bucketlist, {
    'items': fields.List(fields.Nested(bucketlist_item_output)),
    'date_modified': fields.DateTime

})

page_of_bucketlist = api.inherit('Page of bucketlist', pagination, {
    'items': fields.List(fields.Nested(bucketlist_with_items))
})

page_of_bucketlist_items = api.inherit('Page of bucketlist item', bucketlist,
                                       pagination,
                                       {'items': fields.List(fields.Nested(bucketlist_item_output))
})

