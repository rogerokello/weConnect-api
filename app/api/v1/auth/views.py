from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify, session
from flask_cors import cross_origin
from app.models.user import User
from app.models.token import Token
from app import db
from flasgger import swag_from
import re
import json
from sqlalchemy.sql.expression import or_, and_
from numbers import Number
from werkzeug.security import generate_password_hash, check_password_hash

class Registration(MethodView):
    """This class registers a new user."""

    #handle post request for this view( url is auth/register)
    @swag_from('../api-docs/register_a_user.yml')
    def post(self):

        #get the json data sent over post as a dictionary
        try:
            #check if it was json data that was sent
            if request.is_json:
                data = request.get_json()
            else:
                
                response = {
                    "message": "Please supply json data",
                    "status": "failure"
                }
                return make_response(jsonify(response)), 400
        except Exception as e:
            response = {
                "message": "An error occured: Here are the details - " + str(e),
                "status": "failure"
            }
            return make_response(jsonify(response)), 500
        
        #ensure that username, email and password keys are provided
        try:
            username = data['username']
            password = data['password']
            email = data['email']
        except KeyError as missing_key:
            response = {
                "message": "Please supply a " + str(missing_key),
                "status": "failure"
            }
            return make_response(jsonify(response)), 400

        #check if username, password or email is empty
        if not(username) or not(password) or not(email): # using not instead
            response = {
                "message": "Please supply a value for username, email and password",
                "status": "failure"
            }
            return make_response(jsonify(response)), 400

        # check if what was got from json for username or password is not a string
        if not isinstance(username, str) or not isinstance(password, str) or not isinstance(email, str):
            response = {
                'message': 'Please supply string values for username, email and password',
                "status": "failure"
            }
               
            return make_response(jsonify(response)), 401

        #check if email is not in the right format        
        if re.search(r'[\w\.-]+@[\w\.-]+', email) is None:
            response = {
                "message": "Please supply a valid email address",
                "status": "failure"
            }
            return make_response(jsonify(response)), 400

        # Check to see if the user already exists
        user = User.query.filter(or_(User.username==data['username'], User.email==data['email'])).first()

        if user is not None:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                "message": 'User already exists. Please login.',
                "status": "failure"
            }

            return make_response(jsonify(response)), 401

        try:
            # Register the user
            username = data['username']
            password = generate_password_hash(data['password'])
            email = data['email']

            new_user = User(username=username, email=email, password=password)
            new_user.add()

            response = {
                "message": 'You registered successfully. Please log in.',
                "status": "success"
            }
            # return a response notifying the user that they registered successfully
            return make_response(jsonify(response)), 201
        except Exception as e:
            # An error occured, therefore return a string message containing the error
            response = {
                "message": "An error occurred, these are the details: " + str(e),
                "status": "failure"
            }
            return make_response(jsonify(response)), 500


class Login(MethodView):
    """This class-based view handles user login"""
    @swag_from('../api-docs/login_a_user.yml')
    def post(self):
        #Handle POST request for this view. Url ---> /auth/login
        """Endpoint to login a user"""
        try:
            #check if the request is json data
            if request.is_json:
                #get the json data sent over post as a dictionary
                data = request.get_json()
            else:
                response = {
                    "message": "Please supply json data",
                    "status": "failure"
                }
                return make_response(jsonify(response)), 400

            if (isinstance(data['username'], Number)) or (isinstance(data['password'], Number)):
                response = {
                    "message": "Invalid values supplied, Please try again with text values",
                    "status": "failure"
                }
                return make_response(jsonify(response)), 401

            if (not isinstance(data['username'], str)) and (not isinstance(data['password'], str)):
                response = {
                    "message": "Invalid values supplied, Please try again with text values",
                    "status": "failure"
                }
                return make_response(jsonify(response)), 401
                        
            user = User.query.filter(
                            or_(User.username == data['username'],User.email == data['username'])).first()

            #Verify correct password supplied
            if user is None or \
                check_password_hash(user.password, data['password']) is False:
                # User does not exist
                response = {
                    "message": 'Invalid username or password, Please try again',
                    "status": "failure"
                }
                return make_response(jsonify(response)), 401


            user.logged_in = 1

            access_token = User.generate_token(user.id)

            db.session.commit()

            #store token in the Tokens table
            token = Token(token=access_token.decode())
            db.session.add(token)
            db.session.commit()
            
            if access_token is not None:
                response = {
                    "message": 'You logged in successfully.',
                    "access_token": access_token.decode(),
                    "status": "success",
                    "id": user.id,
                    "username": user.username,
                    "email":user.email
                }

                return make_response(jsonify(response)), 200               

        except json.JSONDecodeError:
            response = {
                "message": "Please supply a correct format for your json data",
                "status": "failure"
            }
            return make_response(jsonify(response)), 400

        except KeyError as key:    
            #username or password key is not supplied
            response = {
                "message": "Please supply a " + str(key),
                "status": "failure"
            }

            return make_response(jsonify(response)), 400

        except Exception as e:
            
            response = {
                "message": "Server error: "+ str(e),
                "status": "failure"
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class Logout(MethodView):
    """This class-based view handles user logout"""
    @swag_from('../api-docs/logout_a_user.yml')
    def post(self):
        #Handle POST request for this view. Url ---> /auth/logout
        """Endpoint to logout a user"""
        try:
            # get auth token
            auth_header = request.headers.get('Authorization')

            auth_token = None

            if auth_header and len(auth_header.split(" ")) > 1:
                auth_token = auth_header.split(" ")[1]
            
            if auth_token is None:
                return make_response(jsonify({
                    "message": "Token required",
                    "status": "failure"
                })), 403

            if auth_token is not None:
                #decode the token that was stored after login to extract the user id
                user_id = User.get_token_user_id(auth_token)

                if user_id == "Expired token. Please login to get a new token":
                    
                    #First check if token exists in the Token table
                    token = Token.query.filter_by(token=auth_token).first()

                    # Delete token from the logged in user's table if it is in the logged in user table
                    if token is not None:
                        Token.delete_token(token)

                    return make_response(jsonify(
                                {
                                    "message": " Token Expired. Please login to get a new one",
                                    "status": "failure"
                                }
                    )), 403

                if user_id == "Invalid token. Please register or login":
                    return make_response(jsonify(
                                {
                                    "message": " Invalid Token. Please login to get a new one",
                                    "status": "failure"
                                }
                    )), 403

                #check if token exists in the Token table
                token = Token.query.filter_by(token=auth_token).first()
                
                #Use the user ID that was decoded from the token to extract
                # the user so u can change the logged in flag to 0
                user = User.query.filter_by(id=int(user_id)).first()
                
                #check if the token is stored in the table with tokens
                if token is not None:

                    #remove the token from the token table
                    Token.delete_token(token)

                    #set the user logged in flag to 0
                    user.logged_in = 0
                    user.save()

                    # create the response
                    response = {
                        "message": 'Logout Successful',
                        "status": "success"
                    }
                    # send the response
                    return make_response(jsonify(response)), 201
                else:
                    #log out user if not already logged out
                    response = {
                        "message": 'No need you are already logged out',
                        "status": "success"
                    }
                    
                    #make and send the response
                    return make_response(jsonify(response)), 303

        except Exception as e:

            response = {
                "message": " Internal server error " + str(e),
                "status": "failure"
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class Reset_password(MethodView):
    """This class-based view handles password resetting"""
    @swag_from('../api-docs/reset_password.yml')
    def post(self):
        #Handle POST request for this view. Url ---> /auth/reset-password
        """Endpoint to reset"""
        try:
            # get auth token
            auth_header = request.headers.get('Authorization')
            
            auth_token = None

            if auth_header and len(auth_header.split(" ")) > 1:
                auth_token = auth_header.split(" ")[1]

            if auth_token is None:
                return make_response(jsonify(
                    {
                        "message": "Token required",
                        "status": "failure"
                    }
                )), 403

            
            if auth_token is not None:
                if request.is_json:
                    data = request.get_json()
                    previous_password = data['previous_password']
                    new_password = data['new_password']

                    if not isinstance(previous_password, str) or not isinstance(new_password, str):
                        response = {
                            "message": "Sorry, password reset unsuccessful. Please supply string values",
                            "status": "failure"
                        }
                        return make_response(jsonify(response)), 401

                    if new_password == "":
                        response = {
                            "message": "Please supply a value for your new password",
                            "status": "failure"
                        }
                        return make_response(jsonify(response)), 400
                else:
                    response = {
                        "message": 'Please supply json data',
                        "status": "failure"
                    }
                    #make and send the response
                    return make_response(jsonify(response)), 400

                #decode the token that was stored after login to 
                # extract the user id
                user_id = User.get_token_user_id(auth_token)

                if user_id == "Expired token. Please login to get a new token":
                    return make_response(jsonify(
                                {
                                    "message": " Token Expired. Please login to get a new one",
                                    "status": "failure"
                                }
                    )), 403

                if user_id == "Invalid token. Please register or login":
                    return make_response(jsonify(
                                {
                                    "message": " Invalid Token. Please login to get a new one",
                                    "status": "failure"
                                }
                    )), 403

                #check if token exists in the Token table
                token = Token.query.filter_by(token=auth_token).first()
                
                
                if token is not None:
                    #Reset the user password 
                                   
                    #check if the user with that id and password exist
                    user = User.query.filter_by(id=int(user_id)).first()

                    if user is not None and \
                        check_password_hash(user.password, previous_password) is True:
                        
                        #change the password
                        user.password = generate_password_hash(new_password)
                        
                        # make your changes permanent(Commit)
                        user.save()

                        response = {
                            "message": 'Password reset Successful',
                            "status": "success"
                        }
                        #make and send the response
                        return make_response(jsonify(response)), 201
                    else:
                        response = {
                            "message": "Invalid previous password",
                            "status": "failure"
                        }
                        #make and send the response
                        return make_response(jsonify(response)), 401
                else:
                    response = {
                            "message": "Password reset unsuccessful",
                            "status": "failure"
                    }
                        #make and send the response
                    return make_response(jsonify(response)), 401
        except Exception as e:

            response = {
                "message": " Internal server error " + str(e),
                "status": "failure"
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500
    

# Define the API resource
registration = Registration.as_view('registration')
login = Login.as_view('login')
logout = Logout.as_view('logout')
reset_password = Reset_password.as_view('reset_password')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration,
    methods=['POST'])

# Define the rule for the login url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login,
    methods=['POST'])

# Define the rule for the logout url --->  /auth/logout
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout,
    methods=['POST'])

# Define the rule for the reset password url --->  /auth/reset-password
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=reset_password,
    methods=['POST'])