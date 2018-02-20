from flask import Flask
from . import db

def create_app():
    app = Flask(__name__)
    from .models import Business
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
       return make_response(jsonify({'message': 'not implemented yet'})), 404

    return app