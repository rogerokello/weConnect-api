#from .db import businesses, reviews, users, blacklisted_tokens
from app import db, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta

class User(db.Model):
    #the fields of the User table
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    password = db.Column(db.String(64))
    logged_in = db.Column(db.Integer)
    businesses = db.relationship('Business', backref='creator', lazy='dynamic')

    # create user object
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.logged_in = 0

    #Create a method to add the business
    def add(self):
       db.session.add(self)
       db.session.commit()

    #create a method to save the business
    def save(self):
        db.session.commit()

    @classmethod
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

class Loggedinuser(db.Model):
    #fields
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text())

    # create token object
    def __init__(self, token):
        self.token = token

    #Create a class method to add the token
    def add(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def delete_token(self, token):
        db.session.delete(token)
        db.session.commit()

class Business(db.Model): 

    #the fields of the Business table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64))
    location = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    reviews = db.relationship('Review', backref='creator', lazy='dynamic')

    #initialise business   
    def __init__(self, name, category, location):
        """Initialize the business with a name, category and location."""
        self.name = name
        self.category = category
        self.location = location

    def add(self):
        db.session.add(self)
        db.session.commit()



class Review(db.Model):
    #the fields of the Review table
    id = db.Column(db.Integer, primary_key=True)
    review_summary = db.Column(db.String(64), index=True, unique=True)
    review_description = db.Column(db.String(150))
    star_rating = db.Column(db.String(10))
    business_id = db.Column(db.Integer, db.ForeignKey('business.id'))

    # create a review object
    def __init__(self, review_summary, review_description,
                star_rating, business_id):
        self.review_summary = review_summary
        self.review_description = review_description
        self.star_rating = star_rating
        self.business_id = business_id






