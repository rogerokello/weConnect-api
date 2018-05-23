import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """

    def test_it_works(self):
        """Test the API can get all business registered businesses (GET request)"""

        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that XEDROX string in returned json response
        self.assertIn('Xedrox', str(response.data))
    
    def test_no_business(self):
        """Test the API works when no businesses are available (GET request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that an empty list is in returned json response
        self.assertEqual([], json.loads(response.data.decode())["message"])

    def test_no_token(self):
        """Test the API can get all businesses works when no token is supplied (GET request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    #headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Token required string in returned json response
        self.assertIn('Please provide an Authorisation header', str(response.data))

    def test_invalid_token(self):
        """Test the API can get all businesses works when invalid token is supplied (GET request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token + "5432fr")
                                    )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Token required string in returned json response
        self.assertIn('Invalid Token', str(response.data))   