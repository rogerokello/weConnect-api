from .db import businesses, reviews, users, blacklisted_tokens
from app import current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class Business(): 
    #initialise business   
    def __init__(self, name, category, location):
        """Initialize the business with an name, category and location."""
        self.name = name
        self.category = category
        self.location = location

    #Create a class method to add the business
    @classmethod
    def add(self, business):
        businesses.append(business)

    # return all businesses as a list of dictionary items
    # which you will return jsonify to return
    @classmethod
    def get_all(self):
        current_businesses = []
        for counter,business in enumerate(businesses):
            a_business = {
                'id' : counter,
                'name' : business.name,
                'category': business.category,
                'location': business.location 
            }
            current_businesses.append(a_business)
        
        return current_businesses

    #Method to check if a business ID exists
    @classmethod
    def id_exists(self, business_id = None):
        try:
            businesses[int(business_id)]
        except IndexError:
            return False

        try:
            businesses[int(business_id)]
        except ValueError:
            return False

        return True

    #Method to get biz by id
    @classmethod
    def get_by_id(self, id):
        return businesses[id]

    #Method to delete a biz by id
    @classmethod
    def delete(self, id=None):
        if id is not None:
            businesses.pop(int(id))
            return id
        else:
            return None

    #Method to update a business given its id
    @classmethod
    def update(self, id, name, category, location):
        if self.id_exists(id):
            business_to_update = self.get_by_id(id)
            business_to_update.name = name
            business_to_update.category = category
            business_to_update.location = location
            return True
        else:
            return False

class Review():
    # create a review object
    def __init__(self, review_summary, review_description,
                star_rating, business_id):
        self.review_summary = review_summary
        self.review_description = review_description
        self.star_rating = star_rating
        self.business_id = business_id

    # add review object to database
    @classmethod
    def add(self, a_review):
        reviews.append(a_review)

    # return all reviews as a list of dictionary items
    # which you will return jsonify to return
    @classmethod
    def get_all_business_reviews(self, id):
        business_reviews = []
        for counter,one_review in enumerate(reviews):
            #check for reviews with same business id
            if int(one_review.business_id) == int(id):
                #dict to store review
                a_review = {
                    'review_summary' : one_review.review_summary,
                    'review_description' : one_review.review_description,
                    'star_rating': one_review.star_rating,
                    'business_id': one_review.business_id 
                }
                #attach what was found into business reviews
                business_reviews.append(a_review)
        #return an object you can easily jsonify when sending back
        return business_reviews

class User():
    # create user object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = False
        self.active = True

    # method to add user to the datbase
    @classmethod
    def add(self, a_user):
        users.append(a_user)

    # method to find user by username
    @classmethod
    def get_by_username(self, username):
        for user in users:
            if user.username == username:
                return user

        return False

    #method to return user id
    def get_user_id(self):
        for id, user in enumerate(users):
            if user.username == self.username:
                return id
        return None

    #method to return user id by token
    def get_user_id_given_token(self, token):
        """ Gets and id given the token """
        return self.decode_token(token)
    
    #check if password is valid
    def check_password_is_valid(self, password):
        if self.password == password:
            return True
        else:
            return False

    #check if user already logged in
    def check_already_logged_in(self):
        if self.logged_in:
            return True
        else:
            return False

    #loggin user and change login status to logged in
    def login_user(self):
        self.logged_in = True

    #logout user and change login status
    def logout_user(self):
        self.logged_in = False

    def generate_token(self, user_id):
        """ Generates the access token"""

        try:
            # set up a payload with an expiration time
            payload = {
                'exp': datetime.utcnow() + timedelta(minutes=20),
                'iat': datetime.utcnow(),
                'sub': user_id
            }
            # create the byte string token using the payload and the SECRET key
            jwt_string = jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY'),
                algorithm='HS256'
            )
            return jwt_string

        except Exception as e:
            # return an error in string format if an exception occurs
            return str(e)

    @staticmethod
    def decode_token(token):
        """Decodes the access token from the Authorization header."""
        try:
            # try to decode the token using our SECRET variable
            payload = jwt.decode(token, current_app.config.get('SECRET_KEY'),algorithms='HS256')
            return payload['sub']
        except jwt.ExpiredSignatureError:
            # the token is expired, return an error string
            return "Expired token. Please login to get a new token"
        except jwt.InvalidTokenError:
            # the token is invalid, return an error string
            return "Invalid token. Please register or login"

    @classmethod
    def get_user_by_token(self, token):
        for counter, user in enumerate(users):
            if str(counter) == str(user.decode_token(token)):
                return user
        return None

    def reset_password(self, old_password , new_password):
        if old_password == self.password:
            self.password = new_password
            return "success"
        else:
            return "Please supply correct old password"
