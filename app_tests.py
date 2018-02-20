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

    def test_new_business_can_be_added(self):
        """Test the API can create a business (POST request)"""
        
        response = self.client().post('/businesses', 
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)
        
        # check that Created business string in returned json response
        self.assertIn('Created business: ', str(response.data))

if __name__ == "__main__":
    unittest.main()