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
        
        #create a dict to be used to edit business
        self.edited_business = {'name':'Megatrends',
                                'category': 'Confectionary',
                                'location' : 'Kampala'
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

    def test_api_can_get_all_businesses(self):
        # first add a business
        self.client().post('/businesses', 
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Xedrox string in returned json response
        self.assertIn('Xedrox', str(response.data))

    def test_api_can_get_business_by_id(self):
        # first add a business
        self.client().post('/businesses', 
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses/0')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Xedrox string in returned json response
        self.assertIn('Xedrox', str(response.data))

    def test_api_can_remove_a_business_by_id(self):
        # first add a business
        self.client().post('/businesses', 
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        response = self.client().delete('/businesses/0')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Business deleted string in returned json response
        self.assertIn('Business deleted', str(response.data))

    def test_api_can_modify_a_business_profile(self):
        # first add a business
        self.client().post('/businesses',
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        # Edit business 
        response = self.client().put('/businesses/0',
                            data=json.dumps(self.edited_business),
                            content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Megatrends string in returned json response
        self.assertIn('Megatrends', str(response.data))
        



if __name__ == "__main__":
    unittest.main()