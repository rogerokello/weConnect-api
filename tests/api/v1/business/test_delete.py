import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """

    def test_delete_by_id(self):
        """Test the API can remove a business given an id (DELETE request)"""
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
        
        #delete the business by its id
        response = self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Business deleted string in returned json response
        self.assertIn('Business deleted', str(response.data))


    def test_no_id_provided(self):
        """Test the API can remove a business given an id works when id is not found (DELETE request)"""
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
        
        #delete the business by its id
        self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #delete the business by its id
        response = self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 404)

        # check that Business was not found in returned json response
        self.assertIn('Business was not found', str(response.data))

    def test_no_token_provided(self):
        """Test the API can remove a business given an id works when no token is found (DELETE request)"""
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
        
        #delete the business by its id
        response = self.client().delete('/businesses/0',
                                        #headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Token required in returned json response
        self.assertIn('Please provide an Authorisation header', str(response.data))

    def test_invalid_token_provided(self):
        """Test the API can remove a business given an id works when invalid token is used (DELETE request)"""
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
        
        #delete the business by its id
        response = self.client().delete('/businesses/0',
                                        headers=dict(Authorization="Bearer " + access_token + "ininitfytfty7y8")
                                        )

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Invalid Token in returned json response
        self.assertIn('Invalid Token', str(response.data))
    