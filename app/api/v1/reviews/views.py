from . import reviews_blueprint
from app.models.user import User
from app.models.loggedinuser import Loggedinuser
from app.models.business import Business
from app.models.review import Review, db
from flasgger import swag_from
from flask import request, jsonify, make_response

#review a business given its ID in the url
@reviews_blueprint.route('/businesses/<int:id>/reviews', methods=['POST'])
@swag_from('../api-docs/review_a_business_given_its_id.yml')
def review_a_business_given_its_id(id):

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
            found_business = Business.query.get(id)

            #check if the user id from the decoded token exists in the db
            found_user = User.query.get(int(user_id))

            if found_business:
                # get the data that was sent in the request
                data = request.get_json()

                #create review object
                a_review = Review(
                    review_summary = data['review_summary'],
                    review_description = data['review_description'],
                    star_rating = data['star_rating'],
                    creator = found_user,
                    business = found_business
                )

                #add review to the database
                
                db.session.add(a_review)
                db.session.commit()

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
@reviews_blueprint.route('/businesses/<int:id>/reviews', methods=['GET'])
@swag_from('../api-docs/get_business_reviews_given_its_id.yml')
def get_business_reviews_given_its_id(id):

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
                # get all the reviews for this business currently available
                business_reviews = Review.query.filter_by().all()
                matching_reviews_found = []
                if len(business_reviews) > 0:
                    for a_review in business_reviews:
                        if a_review.business_id == found_business.id:
                            matching_reviews_found.append({
                                'review_summary': a_review.review_summary,
                                'review_description': a_review.review_description,
                                'star_rating': a_review.star_rating
                            })
                    response = {
                        'Reviews': matching_reviews_found
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