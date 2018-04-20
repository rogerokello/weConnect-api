import unittest
import json
from app import create_app, db, session
from tests.api.v1 import BaseTestCase

class AuthTestCase(BaseTestCase):
    """Test case for the authentication blueprint."""

    def test_logout(self):
        """Test the logout works (POST request)"""

        self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                            )

        login_res = self.client().post('/auth/login',
                                        data=json.dumps(self.user_data),
                                        content_type='application/json'
                                        )

        result = json.loads(login_res.data.decode())
        

        response = self.client().post('/auth/logout',
                                headers=dict(Authorization="Bearer " + result['access_token']),
                                content_type='application/json')

        # check that Token required string in returned json response
        self.assertIn('Logout Successful', str(response.data))
        
        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

    def test_logout_no_token(self):
        """Test the API refuses to logout a user because of no token (POST request)"""
        
        response = self.client().post('/auth/logout',
                                content_type='application/json')

        # check that Token required string in returned json response
        self.assertIn('Token required', str(response.data))
        
        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

    def test_logout_already_logged_out(self):
        """Test logout works when someone already logged out(POST request)"""

        self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                            )

        login_res = self.client().post('/auth/login',
                                        data=json.dumps(self.user_data),
                                        content_type='application/json'
                                        )

        result = json.loads(login_res.data.decode())
        
        self.client().post('/auth/logout',
                                headers=dict(Authorization="Bearer " + result['access_token']),
                                content_type='application/json')

        response = self.client().post('/auth/logout',
                                headers=dict(Authorization="Bearer " + result['access_token']),
                                content_type='application/json')

        # check that Token required string in returned json response
        self.assertIn('No need you are already logged out', str(response.data))
        
        #check that a 303 response status code was returned
        self.assertEqual(response.status_code, 303)