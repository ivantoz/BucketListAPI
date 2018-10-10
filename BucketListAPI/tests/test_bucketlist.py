import unittest
import json
from BucketListAPI.tests.base import BaseTestCase
from BucketListAPI.tests.test_auth import register_user
from BucketListAPI.model import Bucketlist, BucketListItem


def create_bucketlist(self, name, token):
    """ creates bucketlist """
    return self.client.post('/api/v1/bucketlist/',
                            data=json.dumps(dict(name=name)),
                            content_type='application/json',
                            headers={'X-API-TOKEN': token},
                            )


class TestBucketlistBlueprint(BaseTestCase):
    """ Test cases for Bucketlist blueprint"""
    def test_create_bucketlist(self):
        """ Test the route to create bucketlist  """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Climb Mount Kenya'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            self.assertTrue(bucketlist_data['message'] == 'Bucketlist successfully created.')
            self.assertTrue(bucketlist_data['bucketlist'])
            self.assertTrue(bucketlist_data['bucketlist']['name'] == name)
            self.assertTrue(bucketlist_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_resp.status_code, 201)
            self.assertEqual(Bucketlist.query.count(), 1)

            # test create bucketlist with empty name
            empty_name = ' '
            bucketlist_empty_name_resp = create_bucketlist(self, empty_name, token)
            bucketlist_empty_name_data = json.loads(bucketlist_empty_name_resp.data.decode())
            self.assertTrue(
                bucketlist_empty_name_data['message']['message'] == 'Input payload validation failed')
            self.assertTrue(
                bucketlist_empty_name_data['message']['field'] == "'name' is a required property")
            self.assert400(bucketlist_empty_name_resp)

    def test_create_bucketlist_item(self):
        """ Test the route to create bucketlist item """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Climb Mountain'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_id = bucketlist_data['bucketlist']['id']
            url = '/api/v1/bucketlist/{}/item/'.format(int(bucketlist_id))
            name = 'Sign up for mountain climbing'
            done = False
            item = json.dumps(dict(name=name, done=done))
            bucketlist_item_resp = self.client.post(url,
                                                    data=item,
                                                    content_type='application/json',
                                                    headers={'X-API-TOKEN': token},
                                                    )
            bucketlist_item_data = json.loads(bucketlist_item_resp.data.decode())
            self.assertTrue(bucketlist_item_data['status'] == 'success')
            self.assertTrue(
                bucketlist_item_data['message'] == 'Bucketlist item successfully created.')
            self.assertTrue(bucketlist_item_data['bucketlist_item'])
            self.assertTrue(bucketlist_item_data['bucketlist_item']['name'] == name)
            self.assertTrue(bucketlist_item_data['bucketlist_item']['done'] == done)
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)
            self.assertEqual(BucketListItem.query.count(), 1)

            # test creating bucketlist item with invalid bucketlist id
            invalid_url = '/api/v1/bucketlist/100/item/'
            bucketlist_item_resp_invalid_id = self.client.post(invalid_url,
                                                               data=item,
                                                               content_type='application/json',
                                                               headers={'X-API-TOKEN': token},
                                                               )
            bucketlist_item_data_invalid_id = json.loads(
                bucketlist_item_resp_invalid_id.data.decode())
            self.assertTrue(
                bucketlist_item_data_invalid_id['message'] == 'Bucketlist not found')
            self.assert404(bucketlist_item_resp_invalid_id)

    def test_get_all_bucketlist(self):
        """ Tests the route to list all bucketlists """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Climb Mount Kenya'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_resp = self.client.get('/api/v1/bucketlist/',
                                              headers={'X-API-TOKEN': token},
                                              )
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['items'][0]['date_created'])
            self.assertTrue(bucketlist_data['items'][0]['created_by'])
            self.assertTrue(bucketlist_data['items'][0]['id'])
            self.assertTrue(bucketlist_data['items'][0]['name'] == name)
            self.assertTrue(bucketlist_data['page'] == 1)
            self.assertTrue(bucketlist_data['pages'] == 1)
            self.assertTrue(bucketlist_data['per_page'] == 10)
            self.assertTrue(bucketlist_data['total'] == 1)
            self.assertListEqual(bucketlist_data['items'][0]['items'], [])
            self.assertTrue(bucketlist_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_resp.status_code, 200)

    def test_get_single_bucketlist(self):
        """ Tests the route to list single bucketlist """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            url = '/api/v1/bucketlist/100'
            bucketlist_resp_invalid_id = self.client.get(url,
                                              headers={'X-API-TOKEN': token},
                                              )
            invalid_bucketlist_data = json.loads(bucketlist_resp_invalid_id.data.decode())
            self.assertTrue(invalid_bucketlist_data['message'] == '404: Not Found')
            self.assert404(bucketlist_resp_invalid_id)
            name = 'Climb Mount Kenya'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_id = bucketlist_data['bucketlist']['id']
            url = '/api/v1/bucketlist/{}/item/'.format(int(bucketlist_id))
            item_name = 'Sign up for mountain climbing'
            done = False
            item = json.dumps(dict(name=item_name, done=done))
            bucketlist_item_resp = self.client.post(url,
                                                    data=item,
                                                    content_type='application/json',
                                                    headers={'X-API-TOKEN': token},
                                                    )
            bucketlist_item_data = json.loads(bucketlist_item_resp.data.decode())
            self.assertTrue(bucketlist_item_data['status'] == 'success')
            url = '/api/v1/bucketlist/{}'.format(int(bucketlist_id))
            bucketlist_resp = self.client.get(url,
                                              headers={'X-API-TOKEN': token},
                                              )
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['date_created'])
            self.assertTrue(bucketlist_data['id'])
            self.assertTrue(bucketlist_data['created_by'])
            self.assertTrue(bucketlist_data['name'] == name)
            self.assertTrue(bucketlist_data['page'] == 1)
            self.assertTrue(bucketlist_data['pages'] == 1)
            self.assertTrue(bucketlist_data['per_page'] == 10)
            self.assertTrue(bucketlist_data['total'] == 1)
            self.assertTrue(bucketlist_data['items'])
            self.assertTrue(bucketlist_data['items'][0]['name'] == item_name)
            self.assertTrue(bucketlist_data['items'][0]['done'] == done)
            self.assertTrue(bucketlist_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_resp.status_code, 200)

    def test_search_by_name(self):
        """ Test that bucketlist is searched by name """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Hiking'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_resp = self.client.get('/api/v1/bucketlist/?q=Hiking',
                                              headers={'X-API-TOKEN': token},
                                              )
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['items'][0]['date_created'])
            self.assertTrue(bucketlist_data['items'][0]['created_by'])
            self.assertTrue(bucketlist_data['items'][0]['id'])
            self.assertTrue(bucketlist_data['items'][0]['name'] == name)
            self.assertTrue(bucketlist_data['page'] == 1)
            self.assertTrue(bucketlist_data['pages'] == 1)
            self.assertTrue(bucketlist_data['per_page'] == 10)
            self.assertTrue(bucketlist_data['total'] == 1)
            self.assertListEqual(bucketlist_data['items'][0]['items'], [])
            self.assertTrue(bucketlist_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_resp.status_code, 200)

            # test search by name invalid non existent name

            bucketlist_resp = self.client.get('/api/v1/bucketlist/?q=vacation',
                                              headers={'X-API-TOKEN': token},
                                              )
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['message'] == 'bucketlist not found')
            self.assert404(bucketlist_resp)

    def test_update_bucketlist(self):
        """ Test the route to update bucketlist """
        response = register_user(self, 'joe@gmail.com', '123456')
        data_register = json.loads(response.data.decode())
        token = data_register['auth_token']
        name = 'Vacation'
        bucketlist_resp = create_bucketlist(self, name, token)
        bucketlist_data = json.loads(bucketlist_resp.data.decode())
        self.assertTrue(bucketlist_data['status'] == 'success')
        bucketlist_id = bucketlist_data['bucketlist']['id']
        new_name = 'Hiking'
        url = '/api/v1/bucketlist/{}'.format(bucketlist_id)
        bucketlist_resp = self.client.put(url,
                                          data=json.dumps(dict(name=new_name)),
                                          content_type='application/json',
                                          headers={'X-API-TOKEN': token},
                                          )
        bucketlist_data = json.loads(bucketlist_resp.data.decode())
        self.assertTrue(bucketlist_data['status'] == 'success')
        self.assertTrue(bucketlist_data['message'] == 'Bucketlist successfully updated.')
        self.assertTrue(bucketlist_data['bucketlist'])
        self.assertTrue(bucketlist_data['bucketlist']['name'] == new_name)
        self.assertTrue(bucketlist_data['bucketlist']['date_modified'])
        self.assertTrue(response.content_type == 'application/json')
        self.assertTrue(bucketlist_resp.content_type == 'application/json')
        self.assertEqual(bucketlist_resp.status_code, 200)

        # test updating bucketlist with empty name
        empty_name = ' '
        url = '/api/v1/bucketlist/{}'.format(bucketlist_id)
        bucketlist_empty_name_resp = self.client.put(url,
                                                     data=json.dumps(dict(name=empty_name)),
                                                     content_type='application/json',
                                                     headers={'X-API-TOKEN': token},
                                                     )
        bucketlist_empty_name_data = json.loads(bucketlist_empty_name_resp.data.decode())
        self.assertTrue(
            bucketlist_empty_name_data['message']['message'] == 'Input payload validation failed')
        self.assertTrue(
            bucketlist_empty_name_data['message']['field'] == "'name' is a required property")
        self.assert400(bucketlist_empty_name_resp)

    def test_update_bucketlist_item(self):
        """ Test the route to update bucketlist item"""
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Climb Mountain'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_id = bucketlist_data['bucketlist']['id']
            url = '/api/v1/bucketlist/{}/item/'.format(int(bucketlist_id))
            item_name = 'Sign up for mountain climbing'
            done = False
            item = json.dumps(dict(name=item_name, done=done))
            bucketlist_item_resp = self.client.post(url,
                                                    data=item,
                                                    content_type='application/json',
                                                    headers={'X-API-TOKEN': token},
                                                    )
            bucketlist_item_data = json.loads(bucketlist_item_resp.data.decode())
            item_id = bucketlist_item_data['bucketlist_item']['id']
            item_new_name = 'getting ready for mountain climbing'
            new_done = True
            updated_item = json.dumps(dict(name=item_new_name, done=new_done))
            update_url = '/api/v1/bucketlist/{}/item/{}'.format(bucketlist_id, item_id)
            bucketlist_item_update_resp = self.client.put(update_url,
                                                          data=updated_item,
                                                          content_type='application/json',
                                                          headers={'X-API-TOKEN': token},
                                                          )
            updated_bucketlist_item_data = json.loads(bucketlist_item_update_resp.data.decode())
            self.assertTrue(updated_bucketlist_item_data['status'] == 'success')
            self.assertTrue(updated_bucketlist_item_data['message'] == 'Bucketlist item '
                                                                       'successfully updated.')
            self.assertTrue(updated_bucketlist_item_data['bucketlist_item'])
            self.assertTrue(
                updated_bucketlist_item_data['bucketlist_item']['name'] == item_new_name)
            self.assertTrue(
                updated_bucketlist_item_data['bucketlist_item']['done'] == new_done)
            self.assertTrue(updated_bucketlist_item_data['bucketlist_item']['date_modified'])
            self.assertTrue(bucketlist_item_update_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_item_update_resp.status_code, 200)

            # test update with empty name on payload data
            item_new_name = ' '
            updated_item = json.dumps(dict(name=item_new_name, done=new_done))
            update_url = '/api/v1/bucketlist/{}/item/{}'.format(bucketlist_id, item_id)
            bucketlist_item_update_empty_name_resp = self.client.put(update_url,
                                                                     data=updated_item,
                                                                     content_type='application/json',
                                                                     headers={'X-API-TOKEN': token},
                                                                     )
            updated_bucketlist_item_data_empty_name = json.loads(
                bucketlist_item_update_empty_name_resp.data.decode())
            self.assertTrue(
                updated_bucketlist_item_data_empty_name['message']['message'] == 'Input payload '
                                                                                 'validation failed')
            self.assertTrue(
                updated_bucketlist_item_data_empty_name['message']['field'] == "'name' is a "
                                                                               "required property")
            self.assert400(bucketlist_item_update_empty_name_resp)

    def test_delete_bucketlist(self):
        """ test the route to delete bucketlist """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Vacation'
            bucketlist_delete_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_delete_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_id = bucketlist_data['bucketlist']['id']
            url = '/api/v1/bucketlist/{}'.format(bucketlist_id)
            bucketlist_delete_resp = self.client.delete(url,
                                                 headers={'X-API-TOKEN': token},
                                                 )
            self.assertTrue(bucketlist_delete_resp.status_code == 204)
            self.assertTrue(bucketlist_delete_resp.content_type == 'application/json')
            self.assertEqual(Bucketlist.query.count(), 0)

            # test delete invalid bucketlist
            url = '/api/v1/bucketlist/100'
            bucketlist_delete_resp_invalid_id = self.client.delete(url,
                                                                   headers={'X-API-TOKEN': token},
                                                                   )
            self.assert403(bucketlist_delete_resp_invalid_id)

    def test_delete_bucketlist_item(self):
        """ Test the route to delete bucketlist item"""
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data_register = json.loads(response.data.decode())
            token = data_register['auth_token']
            name = 'Vacation'
            bucketlist_resp = create_bucketlist(self, name, token)
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['status'] == 'success')
            bucketlist_id = bucketlist_data['bucketlist']['id']
            url = '/api/v1/bucketlist/{}/item/'.format(int(bucketlist_id))
            item_name = 'Sign up for mountain climbing'
            done = False
            item = json.dumps(dict(name=item_name, done=done))
            bucketlist_item_delete_resp = self.client.post(url,
                                                           data=item,
                                                           content_type='application/json',
                                                           headers={'X-API-TOKEN': token},
                                                           )
            bucketlist_item_data = json.loads(bucketlist_item_delete_resp.data.decode())
            item_id = bucketlist_item_data['bucketlist_item']['id']
            url = '/api/v1/bucketlist/{}/item/{}'.format(bucketlist_id, item_id)
            bucketlist_item_delete_resp = self.client.delete(url,
                                                             headers={'X-API-TOKEN': token},
                                                             )
            self.assertTrue(bucketlist_item_delete_resp.status_code == 204)
            self.assertTrue(bucketlist_item_delete_resp.content_type == 'application/json')
            self.assertEqual(BucketListItem.query.count(), 0)
            self.assertEqual(Bucketlist.query.count(), 1)

            # test delete invalid bucketlist item
            url_invalid_id = '/api/v1/bucketlist/{}/item/100'.format(bucketlist_id)
            bucketlist_ivalid_item_delete_resp = self.client.delete(url_invalid_id,
                                                                    headers={'X-API-TOKEN': token},
                                                                    )
            self.assert403(bucketlist_ivalid_item_delete_resp)

    def test_access_end_point_without_token(self):
        """ Test access endpoint without signed token """
        with self.client:
            name = 'Climb Mount Kenya'
            bucketlist_resp = self.client.post('/api/v1/bucketlist/',
                                               data=json.dumps(dict(name=name)),
                                               content_type='application/json',
                                               )
            bucketlist_data = json.loads(bucketlist_resp.data.decode())
            self.assertTrue(bucketlist_data['message']['status'] == 'fail')
            self.assertTrue(bucketlist_data['message']['message'] == 'Authorization token required')
            self.assertTrue(bucketlist_resp.content_type == 'application/json')
            self.assertEqual(bucketlist_resp.status_code, 401)
            self.assertEqual(Bucketlist.query.count(), 0)


if __name__ == '__main__':
    unittest.main()
