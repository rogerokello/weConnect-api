import unittest
import json
from app import create_app, db, session

class BaseTestCase(unittest.TestCase):
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
        
        #create a dict to be used to add a new biz with values as numbers
        self.a_business_with_some_values_as_numbers = {'name':123,
                            'category': 'IT',
                            'location' : 908
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
            'password': 'okello',
            'email':'rogerokello@gmail.com'
        }

        #password reset details
        self.password_infor = {
            'previous_password': 'okello',
            'new_password': 'james'
        }

        #create a dict to be used to store another user's details
        self.another_users_data = {
            'username': 'james',
            'password': 'otim',
            'email':'jamesotim@gmail.com'
        }

        #bind the app context
        with self.app.app_context():
            # create all tables
            db.create_all()

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # drop all tables
            db.session.remove()
            db.drop_all()

    def _register_user(self, username="roger", password="okello", email="rogerokello@gmail.com"):
        """This helper method helps register a test user."""

        return self.client().post('/auth/register',
                                 data=json.dumps({'username':username, 'password':password, 'email':email}),
                                 content_type='application/json'
                                 )
    
    def _login_user(self, username="roger", password="okello", email="rogerokello@gmail.com"):
        """This helper method helps log in a test user."""
        return self.client().post('/auth/login',
                                        data=json.dumps({'username':username,'password':password, 'email':email}),
                                        content_type='application/json'
                                )

    # helper method to get access token
    def _get_token(self):
        #register user first
        self._register_user()

        #login user
        result = self._login_user()

        # obtain the access token from result
        access_token = json.loads(result.data.decode())['access_token']
        
        return access_token