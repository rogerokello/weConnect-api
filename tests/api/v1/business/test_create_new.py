import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """

    def test_create_new(self):
        """Test the API can create a business (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self._get_token()),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Created business string in returned json response
        self.assertIn('Created business: ', str(response.data))

    def test_create_for_non_string_values(self):
        """Test the API can refuses to create a business when some values are not strings (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self._get_token()),
                                data=json.dumps(self.a_business_with_some_values_as_numbers),
                                content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Created business string in returned json response
        self.assertIn('Please supply only string values', str(response.data))

    def test_for_absent_auth_header(self):
        """Test the API rejects business creation in absence of Authorization (POST request)"""
        
        response = self.client().post('/businesses',
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Created business string in returned json response
        self.assertIn('Please provide an Authorisation header', str(response.data))

    def test_for_invalid_token(self):
        """Test the API rejects business creation when token wrong (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self._get_token() + "489u9j82r"),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Invalid Token string in returned json response
        self.assertIn('Invalid Token', str(response.data))

    def test_same_business_cant_be_created(self):
        """ Test api refuses to create businesses with similar names """
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

        # try to add the same business
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Duplicate business in returned json response
        self.assertIn('Duplicate business', str(response.data))
    