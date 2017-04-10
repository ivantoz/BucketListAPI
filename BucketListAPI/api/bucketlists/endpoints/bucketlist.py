import logging

from flask import request
from flask_restplus import Resource

from BucketListAPI.api.bucketlists.business import create_bucketlist, delete_bucketlist, \
    update_bucketlist
from BucketListAPI.api.bucketlists.serializers import bucketlist, \
    bucketlist_item, page_of_bucketlist, page_of_bucketlist_items
from BucketListAPI.api.bucketlists.business import create_bucketlist_item, update_item, delete_item
from BucketListAPI.api.restplus import api
from BucketListAPI.model import Bucketlist
from BucketListAPI.api.bucketlists.parsers import pagination_arguments
from BucketListAPI.api.restplus import auth_required
from flask import abort, current_app, _app_ctx_stack


log = logging.getLogger(__name__)

ns = api.namespace('bucketlist', description='Operations related to Bucketlist')


@ns.route('/')
class BucketListCollection(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_bucketlist)
    @auth_required
    def get(self):
        """
        List all the created bucket list.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        with current_app.app_context():
            user_data = _app_ctx_stack.user_data
            bucketlist_query = Bucketlist.query.filter_by(created_by=user_data['user_id'])
        bucketlists = bucketlist_query.paginate(page, per_page, error_out=False)
        return bucketlists

    @api.response(201, 'Bucketlist successfully created.')
    @api.expect(bucketlist, validate=True)
    @auth_required
    def post(self):
        """
        Create a new bucket list.
        """
        data = request.json
        return create_bucketlist(data), 201


@ns.route('/<int:id>')
@api.param('id', 'Bucketlist ID')
@api.response(404, 'Bucketlist Item not found.')
class BucketList(Resource):

    @api.expect(pagination_arguments)
    @api.marshal_with(page_of_bucketlist_items)
    @auth_required
    def get(self, id):
        """
        Get single bucket list.
        """
        args = pagination_arguments.parse_args(request)
        page = args.get('page', 1)
        per_page = args.get('per_page', 10)
        with current_app.app_context():
            user_data = _app_ctx_stack.user_data
            created_by = user_data['user_id']
        try:
            bucketlist_query = Bucketlist.query.filter_by(created_by=created_by, id=id)
            if not bucketlist_query.count():
                abort(404)
            bucketlist_items = bucketlist_query[0].items
            bucketlist_items_paginated = bucketlist_items.paginate(page, per_page, error_out=False)
            bucketlist_items_paginated.date_modified = bucketlist_query[0].date_modified
            bucketlist_items_paginated.created_by = bucketlist_query[0].created_by
            bucketlist_items_paginated.id = bucketlist_query[0].id
            bucketlist_items_paginated.date_created = bucketlist_query[0].date_created
            bucketlist_items_paginated.name = bucketlist_query[0].name
            return bucketlist_items_paginated
        except Exception as e:
            abort(404, str(e))


    @api.expect(bucketlist)
    @api.response(204, 'Bucketlist item successfully updated.')
    @auth_required
    def put(self, id):
        """
        Update this bucket list.

        * Specify the ID of the bucketlist to modify in the request URL path.
        """
        data = request.json
        return update_bucketlist(id, data), 204

    @api.response(204, 'BucketList item successfully deleted.')
    @auth_required
    def delete(self, id):
        """
        Delete this single bucket list.

        """

        return delete_bucketlist(id), 204


@ns.route('/<int:id>/item/')
@api.param('id', 'Bucketlist ID')
@api.response(201, 'Bucketlist item successfully created.')
class BucketlistItemsCollection(Resource):

    @api.expect(bucketlist_item)
    @auth_required
    def post(self, id):
        """
        Create a new item in bucket list.
        """

        return create_bucketlist_item(id, request.json), 201


@ns.route('/<int:id>/item/<int:item_id>')
@api.param('item_id', 'Bucketlist Item ID')
@api.param('id', 'Bucketlist ID')
@api.response(404, 'Item not found.')
class BucketlistItem(Resource):

    @api.expect(bucketlist_item)
    @api.response(204, 'Item successfully updated.')
    @auth_required
    def put(self, id, item_id):
        """
        Update a bucket list item.
        """
        data = request.json
        return update_item(id, item_id, data), 204

    @api.response(204, 'Item successfully deleted.')
    @auth_required
    def delete(self,id, item_id):
        """
        Delete an item in a bucket list.
        """

        return delete_item(id, item_id), 204



