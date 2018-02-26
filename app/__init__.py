from flask import Flask, current_app, session
from . import db
from config import config
from flasgger import Swagger, swag_from

def create_app(config_name):
    app = Flask(__name__)

    #make configuration for swagger
    app.config['SWAGGER'] = {
            'swagger': '2.0',
            'title': 'we-connect-you-api',
            'description': "The we-connect-you app allows you to register a business and\
            make reviews of other businesses",
            'basePath': '/',
            'version': '0.0.1',
            'contact': {
                'Developer': 'Roger Okello',
                'email': 'rogerokello@gmail.com'
            },
            'license': {
                'name': 'MIT'
            },
            'tags': [
                {
                    'name': 'User',
                    'description': 'The basic unit of authentication'
                },
                {
                    'name': 'Business',
                    'description': 'Businesses that you can connect with to get\
                    a service'
                },
                {
                    'name': 'Review',
                    'description': 'A user rating and remarks for a business'
                },
            ]
        }
    
    #initialise app to use swagger for doc strings
    swagger = Swagger(app)

    #get configuration settings to app
    app.config.from_object(config[config_name])

    #apply the configuration settings on app
    config[config_name].init_app(app)

    from .models import Business, Review, User
    from flask import request, jsonify, make_response

    #Route to register a new business
    @app.route('/businesses', methods=['POST'])
    @swag_from('./api-docs/register_a_business.yml')
    def register_a_business():

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:

            # Attempt to decode the token sent and get the User ID
            user_id = User.decode_token(auth_token)

            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:

                #tranform json data got into a dictionary
                data = request.get_json()

                #extract data from each of the dictionary
                #values
                name = data['name']
                category = data['category']
                location = data['location']

                #create a business object
                a_business = Business(name=name,
                                        category=category,
                                        location=location)

                #add business to the non-persistent database
                Business.add(a_business)

                message = "Created business: " + a_business.name + "successfuly"
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 201
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    # route to get all businesses
    @app.route('/businesses', methods=['GET'])
    @swag_from('./api-docs/get_all_businesses.yml')
    def get_all_businesses():

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:

            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:

                # get all the businesses currently available
                current_businesses = Business.get_all()

                if len(current_businesses) > 0:
                    response = {
                        'Your current businesses are: ': current_businesses
                    }
                    return make_response(jsonify(response)), 201
                else:
                    response = {
                        'Message: ': 'Sorry currently no businesses are present'
                    }
                    return make_response(jsonify(response)), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499            
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499


    # route to get a business by ID
    @app.route('/businesses/<int:id>', methods=['GET'])
    @swag_from('./api-docs/get_a_business_by_id.yml')
    def get_a_business_by_id(id):

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:

            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:
                #check if business is there
                if Business.id_exists(id):

                    found_business = Business.get_by_id(id)
                    business_as_a_dict = {
                        'id': id,
                        'name': found_business.name,
                        'category': found_business.category,
                        'location': found_business.location
                    }

                    return make_response(jsonify({'Business found': business_as_a_dict})), 201
                else:
                    return make_response(jsonify({'Message': 'Business was not found'})), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499 
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    #route to delete a business by ID
    @app.route('/businesses/<int:id>', methods=['DELETE'])
    @swag_from('./api-docs/delete_a_business_by_id.yml')
    def delete_a_business_by_id(id):

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:

            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:

                #check if business is there
                if Business.id_exists(id):
                    
                    #invoke delete method of business class
                    Business.delete(id)

                    return make_response(jsonify({'Message': 'Business deleted'})), 201
                else:
                    return make_response(jsonify({'Message': 'Business was not found'})), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499            
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    #route to update a business by ID
    @app.route('/businesses/<int:id>', methods=['PUT'])
    @swag_from('./api-docs/update_a_business_given_its_id.yml')
    def update_a_business_given_its_id(id):

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:
            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:
                #check if business is there
                if Business.id_exists(id):
                    # get the data that was sent in the request
                    data = request.get_json()
                    
                    #invoke delete method of business class
                    update_status = Business.update(id = id,
                                                    name = data['name'],
                                                    category = data['category'],
                                                    location = data['location'])
                    if update_status:
                        return make_response(
                            jsonify(
                                {'Message': 'Business updated to' + data['name']}
                            )
                        ), 201
                    else:
                        return make_response(
                            jsonify(
                                {'Message': 'Failed to update business'}
                            )
                        ), 500
                else:
                    return make_response(jsonify({'Message': 'Business was not found'})), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499 
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    #review a business given its ID in the url
    @app.route('/businesses/<int:id>/reviews', methods=['POST'])
    @swag_from('./api-docs/review_a_business_given_its_id.yml')
    def review_a_business_given_its_id(id):

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:
            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:
                #check if the business is there
                if Business.id_exists(id):
                    # get the data that was sent in the request
                    data = request.get_json()

                    #create review object
                    a_review = Review(
                        review_summary = data['review_summary'],
                        review_description = data['review_description'],
                        star_rating = data['star_rating'],
                        business_id = id
                    )

                    #add review to the database
                    Review.add(a_review)

                    message = "Created review: " + a_review.review_summary + "successfuly"
                    response = {
                        'message': message
                    }

                    return make_response(jsonify(response)), 201

                else:

                    return make_response(jsonify({'Message': 'Business was not found'})), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    #get all business reviews
    @app.route('/businesses/<int:id>/reviews', methods=['GET'])
    @swag_from('./api-docs/get_business_reviews_given_its_id.yml')
    def get_business_reviews_given_its_id(id):

        # get auth token
        auth_header = request.headers.get('Authorization')
        if auth_header:
            auth_token = auth_header.split(" ")[1]
        else:
            auth_token = ''
        
        if auth_token:
            #try to see if you can get a user by a token
            # they are identified with
            if User.get_user_by_token(auth_token) is not None:
                #check if the business is there
                if Business.id_exists(id):
                    # get all the reviews for this business currently available
                    business_reviews = Review.get_all_business_reviews(id)
                    if len(business_reviews) > 0:
                        response = {
                            'Current business reviews are: ': business_reviews
                        }
                        return make_response(jsonify(response)), 201
                    else:
                        response = {
                            'Message: ': 'Sorry currently no reviews are present'
                        }
                        return make_response(jsonify(response)), 404
                else:
                    return make_response(jsonify({'Message': 'Business was not found'})), 404
            else:
                return make_response(jsonify(
                                    {'Token Error': "Invalid Token"}
                        )), 499
        else:
            return make_response(jsonify({'Token Error': "Token required"})), 499

    # import the authentication blueprint and register it on the app
    from .auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    return app