from . import businesses_blueprint
from app.models.user import User
from app.models.loggedinuser import Loggedinuser
from app.models.business import Business, db
from flasgger import swag_from
from flask import request, jsonify, make_response

#Route to register a new business
@businesses_blueprint.route('/businesses', methods=['POST'])
@swag_from('../api-docs/register_a_business.yml')
def register_a_business():
    # get authorisation header
    auth_header = request.headers.get('Authorization')
    if auth_header:
        #pick token after splitting with the bearer
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token is not '':
        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        user_id = User.decode_token(auth_token)

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:
            #tranform json data got into a dictionary
            data = request.get_json()

            #extract data from each of the dictionary
            #values
            name = data['name']
            category = data['category']
            location = data['location']

            # Strip all white spaces from the name
            # and name convert to upper case
            name_in_upper_case = " ".join(name.split()).upper()

            # Check to see if business with that name exists before
            # adding a new business
            business_with_existing_name = Business.query.filter_by(
                                            name=name_in_upper_case).first()

            if business_with_existing_name:
                message = "Duplicate business"
                response = {
                    'message': message
                }
                return make_response(jsonify(response)), 401


            a_user = User.query.get(int(user_id))

            #create a business object
            a_business = Business(name=name_in_upper_case,
                                    category=category,
                                    location=location,
                                    creator=a_user)

            #add business to the persistent database
            db.session.add(a_business)
            Business.add(a_business)

            message = "Created business: " + name + "successfuly"
            response = {
                'message': message
            }
            return make_response(jsonify(response)), 201
        else:
            return make_response(jsonify(
                                {'Token Error': "Invalid Token"}
                    )), 499
    else:
        if auth_token == '':
            return make_response(jsonify({'Token Error': "Token required"})), 499

# route to get all businesses
@businesses_blueprint.route('/businesses', methods=['GET'])
@swag_from('../api-docs/get_all_businesses.yml')
def get_all_businesses():

    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token:

        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        user_id = User.decode_token(auth_token)

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:

            # get all the businesses currently available
            current_businesses = Business.query.all()

            found_business_list = []
            if len(current_businesses) > 0:
                for a_business in current_businesses:
                    found_business_list. append({
                        'id': a_business.id,
                        'name': a_business.name,
                        'location': a_business.location,
                        'category': a_business.location,
                        'user_id': a_business.user_id
                    })

                response = {
                    'Businesses': found_business_list
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
@businesses_blueprint.route('/businesses/<int:id>', methods=['GET'])
@swag_from('../api-docs/get_a_business_by_id.yml')
def get_a_business_by_id(id):

    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token:

        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        user_id = User.decode_token(auth_token)

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:
            #check if business is there
            found_business = Business.query.filter_by(id=id).first()
            if found_business:             
                    
                business_as_a_dict = {
                    'id': found_business.id,
                    'name': found_business.name,
                    'category': found_business.category,
                    'location': found_business.location,
                    'user_id': found_business.user_id
                }

                return make_response(jsonify({'Business': business_as_a_dict})), 201
            else:
                return make_response(jsonify({'Message': 'Business was not found'})), 404
        else:
            return make_response(jsonify(
                                {'Token Error': "Invalid Token"}
                    )), 499 
    else:
        return make_response(jsonify({'Token Error': "Token required"})), 499

#route to delete a business by ID
@businesses_blueprint.route('/businesses/<int:id>', methods=['DELETE'])
@swag_from('../api-docs/delete_a_business_by_id.yml')
def delete_a_business_by_id(id):

    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token:

        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:

            #check if business is there
            found_business = Business.query.filter_by(id=id).first()
            if found_business:
                    
                #Check if the user is the one who created the business
                if found_business.user_id == user_id:
                    #delete the business
                    db.session.delete(found_business)
                    db.session.commit()

                    return make_response(jsonify({'Message': 'Business deleted'})), 201
                else:
                    return make_response(jsonify({'Message': 'Sorry you are not allowed to delete this business'})), 301
            else:
                return make_response(jsonify({'Message': 'Business was not found'})), 404
        else:
            return make_response(jsonify(
                                {'Token Error': "Invalid Token"}
                    )), 499            
    else:
        return make_response(jsonify({'Token Error': "Token required"})), 499

#route to update a business by ID
@businesses_blueprint.route('/businesses/<int:id>', methods=['PUT'])
@swag_from('../api-docs/update_a_business_given_its_id.yml')
def update_a_business_given_its_id(id):

    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token:
        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:
                
            #check if business is there
            found_business = Business.query.filter_by(id=id).first()
            if found_business:
                # get the data that was sent in the request
                data = request.get_json()
                    
                #Begin to update the business
                found_business.name = data['name']
                found_business.category = data['category']
                found_business.location = data['location']

                try:
                    db.session.commit()
                    return make_response(
                        jsonify(
                            {'Message': 'Business updated to' + data['name']}
                        )
                    ), 201
                except Exception as e:
                    return make_response(
                        jsonify(
                            {'Message': 'Failed to update business because of ' + str(e)}
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

#route to search for a business using its name
@businesses_blueprint.route('/businesses/search', methods=['GET'])
#@swag_from('../api-docs/update_a_business_given_its_id.yml')
def search_for_a_business_by_its_name():

    # get auth token
    auth_header = request.headers.get('Authorization')
    if auth_header:
        try:
            auth_token = auth_header.split(" ")[1]
        except Exception as e:
            return make_response(jsonify(
                                {'Token Error': " Token not being sent in the right format: " + str(e)}
            )), 499
    else:
        auth_token = ''
        
    if auth_token:
        #decode the token that was stored after login to extract the user id
        user_id = User.decode_token(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                                {'Token Error': " Token Expired. Please login to get a new one"}
                    )), 499

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                                {'Token Error': " Invalid Token. Please login to get a new one"}
                    )), 499

        #check if token exists in the Loggedinuser table
        a_logged_in_user_token = Loggedinuser.query.filter_by(token=auth_token).first()

        #Use the user ID that was decoded from the token to extract
        # the user so u can check if the logged in flag is set to 1
        user_with_id = User.query.filter_by(id=int(user_id)).first()
        

        #try to see if you can get a user by a token
        # they are identified with
        if a_logged_in_user_token and user_with_id.logged_in == 1:
                
            #check if q in the parameter strings
            if 'q' in request.args: 
                # find the Business with a particular name
                
                business_to_find = Business.query.filter(Business.name.ilike('%'+request.args['q']+'%'))
                   
                if not business_to_find:
                    return make_response(jsonify({'Message': 'No business found'})), 404
                        
                found_business_details = []
                for business in business_to_find:
                    found_business_details.append({
                        "name": business.name,
                        "category": business.category
                    })

                return make_response(jsonify({'message':found_business_details})), 201
            else:
                return make_response(jsonify({'Message': 'No search parameter found'})), 404
        else:
            return make_response(jsonify(
                                {'Token Error': "Invalid Token"}
                    )), 499 
    else:
        return make_response(jsonify({'Token Error': "Token required"})), 499
