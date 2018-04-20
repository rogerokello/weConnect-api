from . import businesses_blueprint
from app.models.user import User
from app.models.token import Token
from app.models.business import Business, db
from flasgger import swag_from
from flask import request, jsonify, make_response
from app.api.v1.validators.general import validate
from sqlalchemy.sql.expression import or_, and_

#Route to register a new business
@businesses_blueprint.route('/businesses', methods=['POST'])
@validate
@swag_from('../api-docs/register_a_business.yml')
def register_a_business():
    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    user_id = User.get_token_user_id(auth_token)

    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()

    if token is None:
        return make_response(jsonify(
                            {
                                "message": "Invalid Token",
                                "status": "failure"
                            }
        )), 403


    # if a_logged_in_user_token and user_with_id.logged_in == 1:
    #tranform json data got into a dictionary
    data = request.get_json()

    #check if the json data value has something that is not a string
    for value in data.values():
        if not isinstance(value, str):
            message = "Please supply only string values"
            response = {
                "message": message,
                "status": "failure"
            }
            return make_response(jsonify(response)), 401


    #extract data from each of the dictionary
    #values
    name = data['name']
    category = data['category']
    location = data['location']

    if name == "" or category == "" or location == "":
        message = "Please supply a name, category and location"
        response = {
            "message": message,
            "status": "failure"
        }
        return make_response(jsonify(response)), 401

    #remove all spaces from the front and end of the name sent
    name = name.strip(' \t\n\r')

    # Check to see if business with that name exists before
    # adding a new business

    business = Business.query.filter_by(
                                    name=name).first()

    if business is not None:
        message = "Duplicate business"
        response = {
            "message": message,
            "status": "failure"
        }
        return make_response(jsonify(response)), 401


    user = User.query.get(int(user_id))

    #create a business object
    new_business = Business(name=name,
                            category=category,
                            location=location,
                            creator=user)

    #add business to the persistent database
    db.session.add(new_business)
    Business.add(new_business)

    message = "Created business: " + name + " successfully"
    response = {
        "message": message,
        "status": "success"
    }
    return make_response(jsonify(response)), 201

# route to get all businesses
@businesses_blueprint.route('/businesses', methods=['GET'])
@validate
@swag_from('../api-docs/get_all_businesses.yml')
def get_business():

    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()

    if token is None:
        return make_response(jsonify(
                            {
                                "message": "Invalid Token",
                                "status": "failure"
                            }
                )), 403

    if 'limit' in request.args:

        try:
            limit = int(request.args['limit'])
        except ValueError:
            # limit parameter is not an integer so return an error response
            # saying that it is not
            response = {
                "message":'Please specify the limit get parameter as an integer',
                "status": "failure"
            }
            return make_response(jsonify(response)), 401

        if limit < 0:
            response = {
                "message":'Please supply a limit parameter greater than 0 or equal to 0',
                "status": "failure"
            }
            return make_response(jsonify(response)), 401

    #### Get only the number of businesses specified by user ####

    # Use the error_out attribute as False to return an empty list 
    # of attributes if the limit parameter exceeds the number of 
    # records in the db

    page=request.args.get('pageNo') or 1
    limit=request.args.get('limit') or 10

    businesses = Business.query.paginate(
                                    per_page=int(limit), page=int(page), error_out=False)
        
    has_next = businesses.has_next
    has_prev = businesses.has_prev
    total_pages = businesses.pages
    total_number_of_items = businesses.total
    current_page = businesses.page

    businesses = businesses.items


    if 'q' in request.args:
        businesses = Business.query.filter(
                    Business.name.ilike('%'+request.args['q']+'%') |
                    Business.location.ilike('%'+request.args['q']+'%') |
                    Business.category.ilike('%'+request.args['q']+'%'))
        businesses = businesses.paginate(
                                    per_page=int(limit), page=int(page), error_out=False)
        has_next = businesses.has_next
        has_prev = businesses.has_prev
        total_pages = businesses.pages
        total_number_of_items = businesses.total
        current_page = businesses.page
        businesses = businesses.items
        
    
    if ('q' not in request.args) and ('limit' not in request.args):
        # get all the businesses currently available
        businesses = Business.query.all()

    business = []

    for each_business in businesses:
        business.append({
            'id': each_business.id,
            'name': each_business.name,
            'location': each_business.location,
            'category': each_business.category,
            'user_id': each_business.user_id
        })

    response = {
        "message": business,
        "status": "success",
        "has_next": has_next,
        "has_prev": has_prev,
        "total_pages": total_pages,
        "total_number_of_items": total_number_of_items,
        "current_page": current_page
    }
    return make_response(jsonify(response)), 201
        


# route to get a business by ID
@businesses_blueprint.route('/businesses/<int:id>', methods=['GET'])
@validate
@swag_from('../api-docs/get_a_business_by_id.yml')
def get_business_by_id(id):

    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]


    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()

    if token is None:
        return make_response(jsonify(
                            {
                                "message": "Invalid Token",
                                "status": "failure"                                    
                            }
                )), 403 

    #check if business is there
    business = Business.query.get(id)

    if business is None:
        return make_response(jsonify(
            {
                "message": 'Business was not found',
                "status": "success"
            }
        )), 404            
            
    business_details = {
        'id': business.id,
        'name': business.name,
        'category': business.category,
        'location': business.location,
        'user_id': business.user_id
    }

    return make_response(jsonify(
        {
            "message": business_details,
            "status": "success"
        }
    )), 201
        

#route to delete a business by ID
@businesses_blueprint.route('/businesses/<int:id>', methods=['DELETE'])
@validate
@swag_from('../api-docs/delete_a_business_by_id.yml')
def delete_business(id):

    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    user_id = User.get_token_user_id(auth_token)

    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()
    
    if token is None:
        return make_response(jsonify(
                    {
                        "message": "Invalid Token",
                        "status": "failure"
                    }
                )), 403

    #check if business is there
    business = Business.query.get(id)

    if business is None:
        return make_response(jsonify(
            {
                "message": 'Business was not found',
                "status": "success"
            }
        )), 404
            
    #Check if the user is not the one who created the business
    if business.user_id is not user_id:
        return make_response(jsonify(
            {
                "message": 'Sorry you are not allowed to delete this business',
                "status": "success"
            }
        )), 301

    #delete the business
    db.session.delete(business)
    db.session.commit()

    return make_response(jsonify(
        {
            "message": 'Business deleted',
            "status": "success"
        }
    )), 201
                    

#route to update a business by ID
@businesses_blueprint.route('/businesses/<int:id>', methods=['PUT'])
@validate
@swag_from('../api-docs/update_a_business_given_its_id.yml')
def update_business(id):

    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    user_id = User.get_token_user_id(auth_token)

    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()
    

    # try to see if you can get a user by a token
    # they are identified with
    if token is None:
        return make_response(jsonify(
                            {
                                "Token Error": "Invalid Token",
                                "status": "failure"
                            }
        )), 403

            
    #check if business is there
    business = Business.query.get(id)
        
    if business is None:
        return make_response(jsonify(
            {
                "message": 'Business was not found',
                "status": "failure"
            }
        )), 404

    #reject update if the user is not the one who created the business
    if business.user_id != int(user_id):
        message = "Sorry update was rejected because you did not create the business"
        response = {
            "message": message,
            "status": "failure"
        }
        return make_response(jsonify(response)), 401

    # get the data that was sent in the request
    data = request.get_json()

    #check if the json data value has something that is not a string
    for value in data.values():
        if not isinstance(value, str):
            message = "Please supply only string values"
            response = {
                "message": message,
                "status": "failure"
            }
            return make_response(jsonify(response)), 401

    
    name = data['name']
    category = data['category']
    location = data['location']

    if name == "" or category == "" or location == "":
        message = "Please supply a name, category and location"
        response = {
            "message": message,
            "status": "failure"
        }
        return make_response(jsonify(response)), 401

    #remove all spaces from the front and end of the name sent
    name = name.strip(' \t\n\r')
 
    # Check if name in the DB mapped by the ID is not the same 
    # as the one sent
    if business.name != name:

        # Perform a search for that biz name to see if it
        # exists.
        duplicate_business = Business.query.filter_by(name=name).first()

        # If it exists, reject the update of biz
        # because it will create duplicate business names
        if duplicate_business is not None:
            return make_response(
                jsonify(
                    {
                        "message": 'Duplicate business',
                        "status": "failure"
                    }
                )
            ), 401

    data['name'] = name;

    #Begin to update the business  
    for key in data.keys():
        setattr(business,key,data[key])
    
    try:
        db.session.commit()
        return make_response(
            jsonify(
                {
                    "message": 'Business updated to ' + data['name'],
                    "status": "success"
                }
            )
        ), 201
    except Exception as e:
        return make_response(
            jsonify(
                {
                    "message": 'Failed to update business because of ' + str(e),
                    "status": "failure"
                }
            )
        ), 500


#route to filter out businesses by their location or category
@businesses_blueprint.route('/businesses/filter', methods=['GET'])
@validate
@swag_from('../api-docs/filter_out_businesses_by_location_or_category.yml')
def filter_by_location_or_category():

    # get authorisation header
    auth_header = request.headers.get('Authorization')

    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    #check if token exists in the Token table
    token = Token.query.filter_by(token=auth_token).first()

    #try to see if you can get a user by a token
    # they are identified with
    if token is None:
        return make_response(jsonify(
                    {
                        "message": "Invalid Token",
                        "status": "failure"
                    }
        )), 403
            
    #check if categoryorlocation in the parameter strings
    if 'categoryorlocation' not in request.args:
        return make_response(jsonify(
            {
                "message": 'No filter parameter found',
                "status": "failure"
            }                
        )), 404

    # find businesses in a particular category or location  
    businesses = Business.query.filter(
        Business.category.ilike('%'+request.args['categoryorlocation']+'%') |
        Business.location.ilike('%'+request.args['categoryorlocation']+'%')
    )
        
    if businesses is None:
        return make_response(jsonify(
            {
                "message": 'No business found',
                "status": "success"
            }
        )), 404
            
    business = []

    for each_business in businesses:
        business.append({
            "id": each_business.id,
            "name": each_business.name,
            "category": each_business.category,
            "location": each_business.location,
            "user_id": each_business.user_id
        })

    return make_response(jsonify(
        {
            "message":business,
            "status": "success"
        }
    )), 201
