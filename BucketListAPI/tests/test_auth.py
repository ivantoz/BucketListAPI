import unittest
import json
from BucketListAPI.tests.base import BaseTestCase


def register_user(self, email, password):
    return self.client.post(
        '/api/v1/auth/register',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


def login_user(self, email, password):
    return self.client.post(
        '/api/v1/auth/login',
        data=json.dumps(dict(
            email=email,
            password=password
        )),
        content_type='application/json',
    )


class AuthorizationTestCase(BaseTestCase):
    def test_registration(self):
        """ Test for user registration """
        with self.client:
            response = register_user(self, 'joe@gmail.com', '123456')
            data = json.loads(response.data.decode())
            self.assertTrue(data['message']['status'] == 'success')
            self.assertTrue(data['message']['message'] == 'Successfully registered.')
            self.assertTrue(data['message']['auth_token'])
            self.assertTrue(response.content_type == 'application/json')
            self.assertEqual(response.status_code, 201)

    def test_auth_status_with_invalid_token(self):
        """ Test for user status with invalid token """
        token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9' \
                '.eyJleHAiOjE0OTE1Njg3ODMsImlhdCI6MTQ5MTU2ODY2M' \
               'ywic3ViIjoxfQ.4szsVPwiJroXXKSA-NtjiqgjCvsGoPSsXdTZQiPbW08'
        response = self.client.get('/api/v1/auth/status', headers={
            'X-API-TOKEN': 'Bearer ' + token})
        data = json.loads(response.data.decode())
        self.assert401(response)
        self.assertEqual(data['message']['status'], 'fail')
        self.assertEqual(data['message']['message'], 'Invalid token. Please log in again.')

if __name__ == '__main__':
    unittest.main()
