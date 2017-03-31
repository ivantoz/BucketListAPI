import logging

from flask import request
from flask_restplus import Resource

from BucketListAPI.api.bucketlists.business import create_bucketlist, delete_bucketlist, \
    update_bucketlist
from BucketListAPI.api.bucketlists.serializers import bucketlist, bucketlist_with_items
from BucketListAPI.api.bucketlists.business import create_bucketlist_item, update_item, delete_item
from BucketListAPI.api.bucketlists.serializers import bucketlist_item
from BucketListAPI.api.restplus import api
from BucketListAPI.model import Bucketlist, BucketListItem
from flask_httpauth import HTTPBasicAuth

log = logging.getLogger(__name__)

ns = api.namespace('bucketlist', description='Operations related to Bucketlist')

auth = HTTPBasicAuth()


@ns.route('/')
class BucketListCollection(Resource):

    # @auth.login_required
    @api.marshal_list_with(bucketlist)
    def get(self):
        """
        List all the created bucket list.
        """
        bucketlist = Bucketlist.query.all()
        return bucketlist

    @api.response(201, 'Bucketlist successfully created.')
    @api.expect(bucketlist, validate=True)
    def post(self):
        """
        Create a new bucket list.
        """
        data = request.json
        create_bucketlist(data)
        return None, 201


@ns.route('/<int:id>')
@api.response(404, 'Bucketlist Item not found.')
class BucketList(Resource):

    @api.marshal_with(bucketlist_with_items)
    def get(self, id):
        """
        Get single bucket list.
        """
        return BucketList.query.filter(BucketList.id == id).one()

    @api.expect(bucketlist)
    @api.response(204, 'Bucketlist item successfully updated.')
    def put(self, id):
        """
        Update this bucket list.

        * Specify the ID of the bucketlist to modify in the request URL path.
        """
        data = request.json
        update_bucketlist(id, data)
        return None, 204

    @api.response(204, 'BucketList item successfully deleted.')
    def delete(self, id):
        """
        Delete this single bucket list.

        """
        delete_bucketlist(id)
        return None, 204


@ns.route('/<int:id>/item/')
@api.response(201, 'Bucketlist item successfully created.')
class BucketlistItemsCollection(Resource):
    @api.expect(bucketlist_item)
    def post(self, id):
        """
        Create a new item in bucket list.
        """
        create_bucketlist_item(id, request.json)
        return None, 201


@ns.route('<int:id>/item/<int:item_id>')
@api.response(404, 'Item not found.')
class BucketlistItem(Resource):

    @api.expect(bucketlist_item)
    @api.response(204, 'Item successfully updated.')
    def put(self, id, item_id):
        """
        Update a bucket list item.
        """
        data = request.json
        update_item(id, item_id, data)
        return None, 204

    @api.response(204, 'Post successfully deleted.')
    def delete(self,id, item_id):
        """
        Delete an item in a bucket list.
        """
        delete_item(id, item_id)
        return None, 204



