import unittest
import json
from app import create_app, db
from tests.api.v1 import BaseTestCase

class BusinessTestCase(BaseTestCase):
    """Test case for the business endpoint """
        
    def test_search_for_biz(self):
        "Test that the api can search for a business using the name q"
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

        #Search using the name
        response = self.client().get('/businesses?q=Xedrox',
                            headers=dict(Authorization="Bearer " + access_token),
                            content_type='application/json')

        # check that XEDROX string in returned json response
        self.assertIn('Xedrox', str(response.data)) 

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)  

    def test_filter_biz_categ(self):
        "Test that the api can fiter businesses using their categories"
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business in the IT category
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Xedrox',
                                    'category': 'IT',
                                    'location' : 'Lira'
                                }
                            ),
                            content_type='application/json')
        
        #Create another business in the Construction category
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Megatrends',
                                    'category': 'Construction',
                                    'location' : 'Lira'
                                }
                            ),
                            content_type='application/json')

        #filter business using the category
        response = self.client().get('/businesses/filter?categoryorlocation=construction',
                            headers=dict(Authorization="Bearer " + access_token),
                            content_type='application/json')

        # check that Construction string in returned json response
        self.assertIn('Construction', str(response.data)) 

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

    def test_filter_biz_locations(self):
        "Test that the api can fiter businesses using their locations"
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business in the IT category
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Xedrox',
                                    'category': 'IT',
                                    'location' : 'Lira'
                                }
                            ),
                            content_type='application/json')
        
        #Create another business located in Kampala
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Megatrends',
                                    'category': 'Construction',
                                    'location' : 'Kampala'
                                }
                            ),
                            content_type='application/json')

        #filter business using the location
        response = self.client().get('/businesses/filter?categoryorlocation=construction',
                            headers=dict(Authorization="Bearer " + access_token),
                            content_type='application/json')

        # check that Kampala string in returned json response
        self.assertIn('Kampala', str(response.data)) 

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

    def test_return_a_no_of_bizs(self):
        "Test that the api can return a specified number of businesses"
        # register a test user, then log them in
        self._register_user()
        result = self._login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business in the IT category
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Xedrox',
                                    'category': 'IT',
                                    'location' : 'Lira'
                                }
                            ),
                            content_type='application/json')
        
        #Create another business located in Kampala
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Megatrends',
                                    'category': 'Construction',
                                    'location' : 'Kampala'
                                }
                            ),
                            content_type='application/json')

        #Create another business located in the US
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'Microsoft',
                                    'category': 'IT',
                                    'location' : 'United States of America'
                                }
                            ),
                            content_type='application/json')

        #Create another business located in Ireland
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(
                                {
                                    'name':'LinkedIn',
                                    'category': 'IT',
                                    'location' : 'Ireland Republic'
                                }
                            ),
                            content_type='application/json')

        #Return 2 businesses
        response = self.client().get('/businesses?limit=2',
                            headers=dict(Authorization="Bearer " + access_token),
                            content_type='application/json')

        # check that only two businesses are returned
        # Along the way deserialise the data sent in the response
        # and convert back to the dictionary sent and extract the 
        # Businesses key to get the values which is a list.
        # Count the number of elements in the list you extracted.
        # Since you requested for 2, there should only be 2 list elements.
        # Since iam using python 3.5, json.loads() needs to convert the response
        # to a string before it can deserialise back to python object
        self.assertEqual(2, len(json.loads(str(response.data, 'utf-8'))["message"]))

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)
    