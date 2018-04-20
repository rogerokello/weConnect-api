from . import reviews_blueprint
from app.models.user import User
from app.models.token import Token
from app.models.business import Business
from app.models.review import Review, db
from flasgger import swag_from
from flask import request, jsonify, make_response
from app.api.v1.validators.general import validate

#review a business given its ID in the url
@reviews_blueprint.route('/businesses/<int:id>/reviews', methods=['POST'])
@validate
@swag_from('../api-docs/review_a_business_given_its_id.yml')
def review_business(id):

    # get auth token
    auth_header = request.headers.get('Authorization')
    
    if len(auth_header.split(" ")) > 1:
        auth_token = auth_header.split(" ")[1]

    user_id = User.get_token_user_id(auth_token)

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

    #check if business is there
    business = Business.query.get(id)

    #check if the user id from the decoded token exists in the db
    user = User.query.get(int(user_id))

    if business is None:
        return make_response(jsonify(
            {
                "message": 'Business was not found',
                "status":"failure"
            }
        )), 404

    # get the data that was sent in the request
    data = request.get_json()

    #create review object
    new_review = Review(
        review_summary = data['review_summary'],
        review_description = data['review_description'],
        star_rating = data['star_rating'],
        creator = user,
        business = business
    )

    #add review to the database
    
    db.session.add(new_review)
    db.session.commit()

    message = "Created review: " + new_review.review_summary + "successfuly"
    response = {
        "message": message,
        "status": "success"
    }

    return make_response(jsonify(response)), 201


#get all business reviews
@reviews_blueprint.route('/businesses/<int:id>/reviews', methods=['GET'])
@validate
@swag_from('../api-docs/get_business_reviews_given_its_id.yml')
def get_reviews(id):

    # get auth token
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
    business = Business.query.filter_by(id=id).first()

    if business is None:
        return make_response(jsonify(
            {
                "message": 'Business was not found',
                "status": 'failure'
            }
        )), 404

    # get all the reviews for this business currently available
    business_reviews = Review.query.filter_by(business_id=business.id).all()
    
    reviews = []

    if business_reviews is None:
        response = {
            "message": 'Sorry currently no reviews are present',
            "status": 'success'
        }
        return make_response(jsonify(response)), 404

    for each_review in business_reviews:
        reviews.append({
            'review_id': each_review.id,
            'review_summary': each_review.review_summary,
            'review_description': each_review.review_description,
            'star_rating': each_review.star_rating,
            'business_id': each_review.business.id,
            'business_name': each_review.business.name,
            'business_category': each_review.business.category,
            'business_location': each_review.business.location
        })

    response = {
        "message": reviews,
        "status": "success"
    }
    return make_response(jsonify(response)), 201