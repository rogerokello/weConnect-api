from flask import Flask
from . import db

def create_app():
    app = Flask(__name__)
    from .models import Business, Review
    from flask import request, jsonify, make_response

    #Route to register a new business
    @app.route('/businesses', methods=['POST'])
    def register_a_business():
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

    # route to get all businesses
    @app.route('/businesses', methods=['GET'])
    def get_all_businesses():
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

    # route to get a business by ID
    @app.route('/businesses/<int:id>', methods=['GET'])
    def get_a_business_by_id(id):

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

    #route to delete a business by ID
    @app.route('/businesses/<int:id>', methods=['DELETE'])
    def delete_a_business_by_id(id):

        #check if business is there
        if Business.id_exists(id):
            
            #invoke delete method of business class
            Business.delete(id)

            return make_response(jsonify({'Message': 'Business deleted'})), 201
        else:
            return make_response(jsonify({'Message': 'Business was not found'})), 404

    #route to update a business by ID
    @app.route('/businesses/<int:id>', methods=['PUT'])
    def update_a_business_given_its_id(id):

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

    #review a business given its ID in the url
    @app.route('/businesses/<int:id>/reviews', methods=['PUT'])
    def review_a_business_given_its_id(id):

        #check if the business is there
        if Business.id_exists(id):
            # get the data that was sent in the request
            data = request.get_json()

            #create review object
            a_review = Review(
                review_summary = data['review_summary'],
                review_description = data['review_description']
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

    return app