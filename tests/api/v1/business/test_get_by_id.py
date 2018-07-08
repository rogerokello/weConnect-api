import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """

    def test_api_can_get_business_by_id(self):
        """Test the API can get a business by ID (GET request)"""
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

        response = self.client().get('/businesses/1',
                                    headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that XEDROX string in returned json response
        self.assertIn('Xedrox', str(response.data))
    
    def test_get_biz_by_id(self):
        """Test the API can get a business by ID works when no biz exists (GET request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses/1',
                                    headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 404)

        # check that Business was not found string in returned json response
        self.assertIn('Business was not found', str(response.data))
    
    def test_get_biz_by_id_no_token(self):
        """Test the API can get a business by ID works when no token supplied (GET request)"""
        # register a test user, then log them in
        self._register_user()
        self._login_user()


        response = self.client().get('/businesses/1')

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Token required string in returned json response
        self.assertIn('Please provide an Authorisation header', str(response.data))

    def test_get_biz_by_id_invalid_token(self):
        """Test the API can get a business by ID works when invalid token supplied (GET request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses/0',
                                    headers=dict(Authorization="Bearer " + access_token + "moinwoe")
                                )

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Invalid Token string in returned json response
        self.assertIn('Invalid Token', str(response.data))