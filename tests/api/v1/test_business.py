import unittest
import json
from app import create_app, db

class BusinessTestCase(unittest.TestCase):
    """Test case for the business endpoint """
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
            'password': 'okello'
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

    def test_new_business_can_be_added(self):
        """Test the API can create a business (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self.get_token()),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Created business string in returned json response
        self.assertIn('Created business: ', str(response.data))

    def test_new_business_with_some_non_string_values_cannot_be_added(self):
        """Test the API can refuses to create a business when some values are not strings (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self.get_token()),
                                data=json.dumps(self.a_business_with_some_values_as_numbers),
                                content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Created business string in returned json response
        self.assertIn('Please supply only string values', str(response.data))

    def test_new_business_creation_rejects_when_token_absent(self):
        """Test the API rejects business creation in absence of token (POST request)"""
        
        response = self.client().post('/businesses',
                                #headers=dict(Authorization="Bearer " + self.get_token()),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Created business string in returned json response
        self.assertIn('Token required', str(response.data))

    def test_new_business_creation_rejects_when_token_invalid(self):
        """Test the API rejects business creation when token wrong (POST request)"""
        
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + self.get_token() + "489u9j82r"),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Invalid Token string in returned json response
        self.assertIn('Invalid Token', str(response.data))

    def test_api_can_get_all_businesses(self):
        """Test the API can get all business registered businesses (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that XEDROX string in returned json response
        self.assertIn('XEDROX', str(response.data))
    
    def test_api_can_get_all_businesses_works_in_absence_of_businesses(self):
        """Test the API works when no businesses are available (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 404)

        # check that Xedrox string in returned json response
        self.assertIn('Sorry currently no businesses are present', str(response.data))

    def test_api_can_get_all_businesses_works_when_no_token_suppiled(self):
        """Test the API can get all businesses works when no token is supplied (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    #headers=dict(Authorization="Bearer " + access_token)
                                    )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Token required string in returned json response
        self.assertIn('Token required', str(response.data))

    def test_api_can_get_all_businesses_works_when_invalid_token_suppiled(self):
        """Test the API can get all businesses works when invalid token is supplied (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses', 
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses',
                                    headers=dict(Authorization="Bearer " + access_token + "5432fr")
                                    )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Token required string in returned json response
        self.assertIn('Invalid Token', str(response.data))

    def test_api_can_get_business_by_id(self):
        """Test the API can get a business by ID (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        response = self.client().get('/businesses/1',
                                    headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that XEDROX string in returned json response
        self.assertIn('XEDROX', str(response.data))
    
    def test_api_can_get_business_by_id_works_when_no_biz_exists(self):
        """Test the API can get a business by ID works when no biz exists (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses/1',
                                    headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 404)

        # check that Business was not found string in returned json response
        self.assertIn('Business was not found', str(response.data))
    
    def test_api_can_get_business_by_id_works_when_no_token_supplied(self):
        """Test the API can get a business by ID works when no token supplied (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses/1',
                                    #headers=dict(Authorization="Bearer " + access_token)
                                )

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Token required string in returned json response
        self.assertIn('Token required', str(response.data))

    def test_api_can_get_business_by_id_works_when_invalid_token_supplied(self):
        """Test the API can get a business by ID works when invalid token supplied (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        response = self.client().get('/businesses/0',
                                    headers=dict(Authorization="Bearer " + access_token + "moinwoe")
                                )

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Invalid Token string in returned json response
        self.assertIn('Invalid Token', str(response.data))

    def test_api_can_remove_a_business_by_id(self):
        """Test the API can remove a business given an id (DELETE request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        response = self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)

        # check that Business deleted string in returned json response
        self.assertIn('Business deleted', str(response.data))


    def test_api_can_remove_a_business_by_id_when_no_business_with_id_found(self):
        """Test the API can remove a business given an id works when id is not found (DELETE request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #delete the business by its id
        response = self.client().delete('/businesses/1',
                                        headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 404 response status code was returned
        self.assertEqual(response.status_code, 404)

        # check that Business was not found in returned json response
        self.assertIn('Business was not found', str(response.data))

    def test_api_can_remove_a_business_by_id_works_when_no_token_supplied(self):
        """Test the API can remove a business given an id works when no token is found (DELETE request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        response = self.client().delete('/businesses/0',
                                        #headers=dict(Authorization="Bearer " + access_token)
                                        )

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Token required in returned json response
        self.assertIn('Token required', str(response.data))

    def test_business_with_same_name_cannot_be_created(self):
        """ Test api refuses to create businesses with similar names """
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        # try to add the same business
        response = self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')

        #check that a 401 response status code was returned
        self.assertEqual(response.status_code, 401)

        # check that Duplicate business in returned json response
        self.assertIn('Duplicate business', str(response.data))

    def test_api_can_remove_a_business_by_id_works_when_invalid_token_supplied(self):
        """Test the API can remove a business given an id works when invalid token is used (DELETE request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        # first add a business
        self.client().post('/businesses',
                                headers=dict(Authorization="Bearer " + access_token),
                                data=json.dumps(self.a_business),
                                content_type='application/json')
        
        #delete the business by its id
        response = self.client().delete('/businesses/0',
                                        headers=dict(Authorization="Bearer " + access_token + "ininitfytfty7y8")
                                        )

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Invalid Token in returned json response
        self.assertIn('Invalid Token', str(response.data))

    def test_api_can_modify_a_business_profile(self):
        """Test the API can modify a business profile (PUT request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

    def test_api_can_modify_a_business_profile_rejects_update_for_number_values(self):
        """Test the API can modify a business profile rejects update for number values (PUT request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

    def test_api_can_modify_a_business_profile_rejects_update_to_existing_biz_name(self):
        """Test the API can modify a business profile rejects when biz name is duplicate (PUT request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

    def test_api_can_modify_a_business_profile_works_when_no_token_supplied(self):
        """Test the API can modify a business profile works when no token supplied (PUT request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

        #check that a 499 response status code was returned
        self.assertEqual(response.status_code, 499)

        # check that Megatrends string in returned json response
        self.assertIn('Token required', str(response.data))

    def test_api_can_create_a_business_review(self):
        """Test the API can create a business review (POST request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

    def test_api_can_get_all_business_review(self):
        """Test the API can get all business reviews (GET request)"""
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        #make the review
        self.client().post('/businesses/1/reviews',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business_review),
                            content_type='application/json')

        #get all the reviews
        response = self.client().get('/businesses/1/reviews',
                                    headers=dict(Authorization="Bearer " + access_token)
                                    )

        # check that Good stuff string in returned json response
        self.assertIn('Good stuff', str(response.data))

    def test_api_can_search_for_business_using_a_name_by_param_q(self):
        "Test that the api can search for a business using the name q"
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

        # obtain the access token
        access_token = json.loads(result.data.decode())['access_token']

        #first create a business
        self.client().post('/businesses',
                            headers=dict(Authorization="Bearer " + access_token),
                            data=json.dumps(self.a_business),
                            content_type='application/json')

        #Search using the name
        response = self.client().get('/businesses/search?q=Xedrox',
                            headers=dict(Authorization="Bearer " + access_token),
                            content_type='application/json')

        # check that XEDROX string in returned json response
        self.assertIn('XEDROX', str(response.data)) 

        #check that a 201 response status code was returned
        self.assertEqual(response.status_code, 201)  

    def test_api_can_filter_businesses_using_their_categories(self):
        "Test that the api can fiter businesses using their categories"
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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

    def test_api_can_filter_businesses_using_their_locations(self):
        "Test that the api can fiter businesses using their locations"
        # register a test user, then log them in
        self.register_user()
        result = self.login_user()

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