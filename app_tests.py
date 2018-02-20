import unittest, json
from flask import request
from app import create_app, db

class WeConnectApiTestCase(unittest.TestCase):

    def setUp(self):
        #create app using the flask import
        self.app = create_app()

        #create a test client
        self.client = self.app.test_client

        #create a dict to be used to add a new biz
        self.a_business = {'name':'Xedrox',
                            'category': 'IT',
                            'location' : 'Lira'
                            }
        #bind the app context
        with self.app.app_context():
            pass

    def tearDown(self):
        """teardown all initialized variables."""
        with self.app.app_context():
            # delete database contents
            db.businesses.clear()

if __name__ == "__main__":
    unittest.main()