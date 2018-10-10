import unittest
from BucketListAPI.tests.base import BaseTestCase
from BucketListAPI.api.auth.business import auth_status, logout


class TestBucketListFunctions(BaseTestCase):
    """ test static functions"""
    def test_auth_status_with_empty_token(self):
        """ Test checking auth status with empty token"""
        token = None
        resp = auth_status(token)
        self.assertEqual(resp[0]['status'], 'fail')
        self.assertEqual(resp[0]['message'], 'Provide a valid auth token.')

    def test_logout_with_empty_token(self):
        """ Test checking auth status with empty token"""
        token = None
        resp = logout(token)
        self.assertEqual(resp[0]['status'], 'fail')
        self.assertEqual(resp[0]['message'], 'Provide a valid auth token.')

if __name__ == '__main__':
    unittest.main()
