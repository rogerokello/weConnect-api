import unittest
import json
from app import create_app, db, session
from tests.api.v1 import BaseTestCase

class AuthTestCase(BaseTestCase):
    """Test case for the authentication blueprint."""

    def test_user_registration(self):
        """Test user registration works correcty. (POST request)"""

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
    
    def test_registration_no_json(self):
        "Test user registration rejects when data supplied is not json (POST request)"
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

    def test_registration_no_username_key(self):
        "Test user registration rejects when no username key supplied (POST request)"
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

    def test_registration_no_passwd_key(self):
        "Test user registration rejects when no password key supplied (POST request)"
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
    
    def test_reg_no_uzname_or_pass_or_email(self):
        "Test user registration rejects when no username or password supplied (POST request)"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"username":"",
                                                "password":"",
                                                "email":""
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a value for username, email and password")
        self.assertEqual(res.status_code, 400)

    def test_reg_invalid_email(self):
        "Test user registration rejects when invalid email supplied (POST request)"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"username":"roger",
                                                "password":"okello",
                                                "email":"rfafd.o"
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply a valid email address")
        self.assertEqual(res.status_code, 400)

    def test_reg_uzname_or_passwd_or_email(self):
        "Test user registration rejects non string supplied for username or password (POST request)"
        #make a request to the register endpoint
        res = self.client().post('/auth/register',
                                data=json.dumps({"username":12,
                                                "password":12334,
                                                "email": 1233
                                }),
                                content_type='application/json'
                                 )
        # get the results returned in json format
        result = json.loads(res.data.decode())

        # assert that the request contains a success message and 
        # a 201 status code
        self.assertEqual(result['message'],
                        "Please supply string values for username, email and password")
        self.assertEqual(res.status_code, 401)