import unittest
import json
from app import create_app, db, session
from tests.api.v1 import BaseTestCase

class AuthTestCase(BaseTestCase):
    """Test case for the authentication blueprint."""
    
    def test_user_login(self):
        """Test registered user can login. (POST request)"""
        
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

    def test_login_when_email_used(self):
        """Test registered user can login with email address used for username. (POST request)"""
        
        #first register a user
        self.client().post('/auth/register',
                                 data=json.dumps(self.user_data),
                                 content_type='application/json'
                            )
        
        #try to login using registration credentials
        login_res = self.client().post('/auth/login',
                                        data=json.dumps({'username':'rogerokello@gmail.com', 'password':'okello'}),
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

    def test_login_empty_json(self):
        "Test user login rejects when data supplied is not json (POST request)"
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
    
    def test_login_no_username_key(self):
        "Test user login rejects when no username key supplied (POST request)"
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

    def test_login_no_passwd_key(self):
        "Test user login rejects when no password key supplied (POST request)"
        #register a user
        self._register_user()
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

    def test_login_invalid_username(self):
        "Test user login rejects invalid username supplied (POST request)"
        #register a user
        self._register_user()
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
        # a 401 status code
        self.assertEqual(result['message'],
                        "Invalid username or password, Please try again")
        self.assertEqual(res.status_code, 401)

    def test_login_non_txt_for_values(self):
        "Test user login rejects non text supplied for values (POST request)"
        #register a user
        self._register_user()
        #make a request to the register endpoint
        res = self.client().post('/auth/login',
                                data=json.dumps({"username":12,
                                                "password":2334
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 401 status code
        self.assertEqual(result['message'],
                        "Invalid values supplied, Please try again with text values")
        self.assertEqual(res.status_code, 401)

    def test_login_username_as_no(self):
        "Test user login rejects username supplied as a number (POST request)"
        #register a user
        self._register_user()
        #make a request to the register endpoint using a number username
        res = self.client().post('/auth/login',
                                data=json.dumps({"username":123,
                                                "password":""
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 401 status code
        self.assertEqual(result['message'],
                        "Invalid values supplied, Please try again with text values")
        self.assertEqual(res.status_code, 401)