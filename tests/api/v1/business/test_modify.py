import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """
    # def setUp(self):
    #     #create app using the flask import
    #     self.app = create_app('testing')

    #     #create a test client
    #     self.client = self.app.test_client

    #     #create a dict to be used to add a new biz
    #     self.a_business = {'name':'Xedrox',
    #                         'category': 'IT',
    #                         'location' : 'Lira'
    #                         }
        
    #     #create a dict to be used to add a new biz with values as numbers
    #     self.a_business_with_some_values_as_numbers = {'name':123,
    #                         'category': 'IT',
    #                         'location' : 908
    #                         }

    #     #create a dict to be used to edit business
    #     self.edited_business = {'name':'Megatrends',
    #                             'category': 'Confectionary',
    #                             'location' : 'Kampala'
    #                         }

    #     #create a dict to be used to store the review
    #     self.a_business_review = {'review_summary':'Good stuff',
    #                             'review_description': 'I liked every thing about it',
    #                             'star_rating' : '5'
    #                         }
                            
    #     #create a dict to be used to store user details
    #     self.user_data = {
    #         'username': 'roger',
    #         'password': 'okello',
    #         'email':'rogerokello@gmail.com'
    #     }

    #     #create a dict to be used to store another user's details
    #     self.another_users_data = {
    #         'username': 'james',
    #         'password': 'otim',
    #         'email':'jamesotim@gmail.com'
    #     }

    #     #bind the app context
    #     with self.app.app_context():
    #         # create all tables
    #         db.create_all()

    # def tearDown(self):
    #     """teardown all initialized variables."""
    #     with self.app.app_context():
    #         # drop all tables
    #         db.session.remove()
    #         db.drop_all()

    # def _register_user(self, username="roger", password="okello", email="rogerokello@gmail.com"):
    #     """This helper method helps register a test user."""

    #     return self.client().post('/auth/register',
    #                              data=json.dumps({'username':username, 'password':password, 'email':email}),
    #                              content_type='application/json'
    #                              )
    
    # def _login_user(self, username="roger", password="okello", email="rogerokello@gmail.com"):
    #     """This helper method helps log in a test user."""
    #     return self.client().post('/auth/login',
    #                                     data=json.dumps({'username':username,'password':password, 'email':email}),
    #                                     content_type='application/json'
    #                             )

    # # helper method to get access token
    # def _get_token(self):
    #     #register user first
    #     self._register_user()

    #     #login user
    #     result = self._login_user()

    #     # obtain the access token from result
    #     access_token = json.loads(result.data.decode())['access_token']
        
    #     return access_token

    def test_modify_biz(self):
        """Test the API can modify a business profile (PUT request)"""
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

        # Edit business 
        response = self.client().put('/businesses/1',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Megatrends string in returned json response
        self.assertIn('Megatrends', str(response.data))

    def test_modify_biz_profile_non_creater(self):
        """Test the API refuses to modify a business profile one did not create (PUT request)"""

        # first add a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + self._get_token()),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        self._register_user(username="james", password="otim", email="jamesotim@gmail.com")
        result1 = self._login_user(username="james", password="otim", email="jamesotim@gmail.com")

        # obtain the access token
        access_token = json.loads(result1.data.decode())['access_token']

        # Try to edit a business the user did not create 
        response = self.client().put('/businesses/1',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Sorry update was rejected  string in returned json response
        self.assertIn('Sorry update was rejected ', str(response.data))

    def test_modify_biz_number_values(self):
        """Test the API can modify a business profile rejects update for number values (PUT request)"""
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

        # Edit business 
        response = self.client().put('/businesses/1',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_with_some_values_as_numbers),
                            content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Megatrends string in returned json response
        self.assertIn('Please supply only string values', str(response.data))

    def test_modify_existing_biz(self):
        """Test the API can modify a business profile rejects when biz name is duplicate (PUT request)"""
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

        # Add another business with a different name
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        # Edit first business added to have same name as an already
        # existing business
        response = self.client().put('/businesses/1',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Megatrends string in returned json response
        self.assertIn('Duplicate business', str(response.data))

    def test_modify_biz_no_token(self):
        """Test the API can modify a business profile works when no token supplied (PUT request)"""
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

        # Edit business 
        response = self.client().put('/businesses/1',
                            #headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 403 response status code was returned
        self.assertEqual(response.status_code, 403)

        # check that Megatrends string in returned json response
        self.assertIn('Please provide an Authorisation header', str(response.data))
    