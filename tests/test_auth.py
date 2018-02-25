import unittest
import json
from app import create_app, db

class AuthTestCase(unittest.TestCase):
    """Test case for the authentication blueprint."""
    def setUp(self):
        #create app using the flask import
        self.app = create_app('testing')

        #create a test client
        self.client = self.app.test_client

        #create a dict to be used to add a new biz
        self.a_business = {'name':'Xedrox',
                            'category': 'IT',
                            'location' : 'Lira'
                            }
        
        #create a dict to be used to edit business
        self.edited_business = {'name':'Megatrends',
                                'category': 'Confectionary',
                                'location' : 'Kampala'
                            }

        #create a dict to be used to store the review
        self.a_business_review = {'review_summary':'Good stuff',
                                'review_description': 'I liked every thing about it',
                                'star_rating' : '5'
                            }
                            
        #create a dict to be used to store user details
        self.user_data = {
            'username': 'roger',
            'password': 'okello'
        }

        #bind the app context
        with self.app.app_context():
            pass

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # delete database contents
            db.businesses.clear()
            db.reviews.clear()
            db.users.clear()

    def register_user(self, username="roger", password="okello"):
        """This helper method helps register a test user."""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                                 )
    
    def login_user(self, username="roger", password="okello"):
        """This helper method helps log in a test user."""
        user_data = {
            'username': username,
            'password': password
        }
        return self.client().post('/auth/login',
                                        data=json.dumps(self.user_data),
                                        content_type='application/json'
                                )

    # helper method to get access token
    def get_token(self):
        #register user first
        self.register_user()

        #login user
        result = self.login_user()

        # obtain the access token from result
        access_token = json.loads(result.data.decode())['access_token']
        
        return access_token

    def test_user_registration_works(self):
        """Test user registration works correcty."""

        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                                 )             
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "You registered successfully. Please log in.")
        self.assertEqual(res.status_code, 201)
    
    def test_user_registration_rejects_json_data_not_supplied(self):
        "Test user registration rejects when data supplied is not json"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({})
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply json data")
        self.assertEqual(res.status_code, 400)

    def test_user_registration_rejects_no_username_key_supplied(self):
        "Test user registration rejects when no username key supplied"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"":""}),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a 'username'")
        self.assertEqual(res.status_code, 400)

    def test_user_registration_rejects_no_password_key_supplied(self):
        "Test user registration rejects when no password key supplied"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"username":""}),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a 'password'")
        self.assertEqual(res.status_code, 400)
    
    def test_user_registration_rejects_no_username_or_password_supplied(self):
        "Test user registration rejects when no username or password supplied"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"username":"",
                                                "password":""
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a values for both username and password")
        self.assertEqual(res.status_code, 400)

    
    def test_user_login_works(self):
        """Test registered user can login."""
        #first register a user
        self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                            )
        
        #try to login using registration credentials
        login_res = self.client().post('/auth/login',
                                        data=json.dumps(self.user_data),
                                        content_type='application/json'
                                        )

        # get the results in json format
        result = json.loads(login_res.data.decode())

        # Test that the response contains success message
        self.assertEqual(result['message'], "You logged in successfully.")

        # Assert that the status code returned is equal to 200
        self.assertEqual(login_res.status_code, 200)

        # Assert that the result has an access token
        self.assertTrue(result['access_token'])

    def test_user_login_rejects_json_data_not_supplied(self):
        "Test user login rejects when data supplied is not json"
        #make a request to the register endpoint
        res = self.client().post('/auth/login',
                                data=json.dumps({})
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply json data")
        self.assertEqual(res.status_code, 400)
    
    def test_user_login_rejects_no_username_key_supplied(self):
        "Test user login rejects when no username key supplied"
        #make a request to the login endpoint
        res = self.client().post('/auth/login',
                                data=json.dumps({"":""}),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a 'username'")
        self.assertEqual(res.status_code, 400)

    def test_user_login_rejects_no_password_key_supplied(self):
        "Test user login rejects when no password key supplied"
        #register a user
        self.register_user()
        #make a request to the login endpoint
        res = self.client().post('/auth/login',
                                data=json.dumps({"username":"roger"}),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a 'password'")
        self.assertEqual(res.status_code, 400)

    def test_user_login_rejects_invalid_username_supplied(self):
        "Test user login rejects invalid username supplied"
        #register a user
        self.register_user()
        #make a request to the register endpoint
        res = self.client().post('/auth/login',
                                data=json.dumps({"username":"",
                                                "password":""
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Invalid username, Please try again")
        self.assertEqual(res.status_code, 401)

    def test_user_logout_works(self):
        """Test the API can logout a user"""
        
        response = self.client().post('/auth/logout',
                                headers=dict(Authorization="Bearer " + self.get_token()),
                                content_type='application/json')

        # check that Logout Successful string in returned json response
        self.assertIn('Logout Successful', str(response.data))
        
        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

    def test_user_logout_rejects_when_no_token_supplied(self):
        """Test the API refuses to logout a user because of no token"""
        
        response = self.client().post('/auth/logout',
                                #headers=dict(Authorization="Bearer " + self.get_token()),
                                content_type='application/json')

        # check that Token required string in returned json response
        self.assertIn('Token required', str(response.data))
        
        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)