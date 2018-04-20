import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """

    def test_create_biz_review(self):
        """Test the API can create a business review (POST request)"""
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        #make the review
        response = self.client().post('/businesses/1/reviews',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_review),
                            content_type='application/json')

        #make the same review
        response = self.client().post('/businesses/1/reviews',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_review),
                            content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Good stuff string in returned json response
        self.assertIn('Good stuff', str(response.data))