import unittest
import json
from app import create_app, db, session
from tests.api.v1 import BaseTestCase

class AuthTestCase(BaseTestCase):
    """Test case for the authentication blueprint."""

    def test_reset_works(self):
        """Test the API can reset a password (POST request)"""
        
        response = self.client().post('/auth/reset-password',
                                headers=dict(Authorization="Bearer " + self._get_token()),
                                data = json.dumps(self.password_infor),
                                content_type='application/json')

        # check that Token required string in returned json response
        self.assertIn('Password reset Successful', str(response.data))
        
        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

    def test_reset_rejects_non_string(self):
        """Test the API reset password component rejects when non string passwords supplied(POST request)"""
        
        response = self.client().post('/auth/reset-password',
                                headers=dict(Authorization="Bearer " + self._get_token()),
                                data = json.dumps({
                                                'previous_password': 123,
                                                'new_password': 123
                                }),
                                content_type='application/json')

        # check that Token required string in returned json response
        test_string = 'Sorry, password reset unsuccessful. Please supply string values'
        self.assertIn(test_string, str(response.data))
        
        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)
