from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify, session
from app.models.user import User
from app.models.loggedinuser import Loggedinuser
from app import db
from flasgger import swag_from

class RegistrationView(MethodView):
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
                    "message": "Please supply json data"
                }
                return make_response(jsonify(response)), 400
        except Exception as e:
            #check if json data conforms to right standard
            if "Failed to decode JSON object" in str(e):
                response = {
                    "message": "Please supply a correct format for your json data"
                }
                return make_response(jsonify(response)), 400
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 400
        
        #ensure that username and password keys are provided
        try:
            username = data['username']
            password = data['password']
        except KeyError as missing_key:
            response = {
                "message": "Please supply a " + str(missing_key)
            }
            return make_response(jsonify(response)), 400

        if data['username'] == "" or data['password'] == "":
            response = {
                "message": "Please supply a values for both username and password"
            }
            return make_response(jsonify(response)), 400

        # Check to see if the user already exists
        user = User.query.filter_by(username=data['username']).first()

        if not user:
            #user does not exist
            try:
                # Register the user
                username = data['username']
                password = data['password']
                user = User(username=username, password=password)
                user.add()

                response = {
                    'message': 'You registered successfully. Please log in.'
                }
                # return a response notifying the user that they registered successfully
                return make_response(jsonify(response)), 201
            except Exception as e:
                # An error occured, therefore return a string message containing the error
                response = {
                    'message': str(e)
                }
                return make_response(jsonify(response)), 401
            
        else:
            # There is an existing user. We don't want to register users twice
            # Return a message to the user telling them that they they already exist
            response = {
                'message': 'User already exists. Please login.'
            }

            return make_response(jsonify(response)), 202

class LoginView(MethodView):
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
                    "message": "Please supply json data"
                }
                return make_response(jsonify(response)), 400

            if isinstance(data['username'], int):
                response = {
                    "message": "Invalid username, Please try again with a username that is not a number"
                }
                return make_response(jsonify(response)), 401

            # Get the user object using their user name
            found_user = User.query.filter_by(username=data['username'], password=data['password']).first()
            # Try to authenticate the found user using their password
            if found_user:

                #change the logged in flag to 1
                found_user.logged_in = 1
                

                # Generate the access token. This will be used as
                # the authorization header
                access_token = User.generate_token(found_user.id)
                db.session.commit()

                #store token in the loggedinusers table
                loggedinuser = Loggedinuser(token=access_token.decode())
                db.session.add(loggedinuser)
                db.session.commit()
                
                if access_token:
                    response = {
                        'message': 'You logged in successfully.',
                        'access_token': access_token.decode()
                    }

                    #return a successful response
                    return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid username or password, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:

            #check if nothing in json request
            if "Failed to decode JSON object:" in str(e):
                response = {
                    "message": "Please supply a correct format for your json data"
                }
                return make_response(jsonify(response)), 400
            
            #check if username or password is not supplied
            if str(e) == "'username'" or str(e) == "'password'":
                response = {
                    'message': "Please supply a " + str(e)
                }

                # Return a server error using the HTTP Error Code 400 (Bad request)
                return make_response(jsonify(response)), 400


            # Create a response containing an string error message
            # incase an exception occurs
            response = {
                'message': str(e)
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class LogoutView(MethodView):
    """This class-based view handles user logout"""
    @swag_from('../api-docs/logout_a_user.yml')
    def post(self):
        #Handle POST request for this view. Url ---> /auth/logout
        """Endpoint to logout a user"""
        try:
            # get auth token
            auth_header = request.headers.get('Authorization')

            if auth_header:
                auth_token = auth_header.split(" ")[1]
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
                
                #check if the token is stored in the table with tokens
                if a_logged_in_user_token:

                    #remove the token from the token table
                    Loggedinuser.delete_token(a_logged_in_user_token)

                    #set the user logged in flag to 0
                    user_with_id.logged_in = 0
                    user_with_id.save()

                    # create the response
                    response = {
                        'message': 'Logout Successful'
                    }
                    # send the response
                    return make_response(jsonify(response)), 201
                else:
                    #log out user if not already logged out
                    response = {
                        'message': 'No need you are already logged out'
                    }
                    
                    #make and send the response
                    return make_response(jsonify(response)), 303
            else:
                return make_response(jsonify({'Token Error': "Token required"})), 499

        except Exception as e:

            response = {
                'message': " Internal server error " + str(e)
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500

class Reset_passwordView(MethodView):
    """This class-based view handles password resetting"""
    @swag_from('../api-docs/reset_password.yml')
    def post(self):
        #Handle POST request for this view. Url ---> /auth/reset-password
        """Endpoint to reset"""
        try:
            # get auth token
            auth_header = request.headers.get('Authorization')
            
            if auth_header:
                auth_token = auth_header.split(" ")[1]
            else:
                auth_token = ''
            
            if auth_token:
                if request.is_json:
                    data = request.get_json()
                    your_previous_password = data['previous_password']
                    your_new_password = data['new_password']
                    if your_new_password == "":
                        response = {
                            "message": "Please supply a value for your new password"
                        }
                        return make_response(jsonify(response)), 400
                else:
                    response = {
                        'message': 'Please supply json data'
                    }
                    #make and send the response
                    return make_response(jsonify(response)), 400

                #decode the token that was stored after login to 
                # extract the user id
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
                
                
                if a_logged_in_user_token and user_with_id.logged_in == 1:
                    #Reset the user password 
                    
                    
                    #check if the user with that id and password exist
                    found_user = User.query.filter_by(id=int(user_id), password=str(your_previous_password)).first()

                    if found_user:
                        #change the password
                        found_user.password = str(your_new_password)
                        
                        # make your changes permanent(Commit)
                        found_user.save()

                        response = {
                            'message': 'Password reset Successful'
                        }
                        #make and send the response
                        return make_response(jsonify(response)), 201
                    else:
                        response = {
                            'message': "Password reset unsuccessful"
                        }
                        #make and send the response
                        return make_response(jsonify(response)), 304
                else:
                    response = {
                            'message': "Invalid previous password"
                    }
                        #make and send the response
                    return make_response(jsonify(response)), 304
            else:
                return make_response(jsonify({'Token Error': "Token required"})), 499

        except Exception as e:

            response = {
                'message': " Internal server error " + str(e)
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500
    

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')
logout_view = LogoutView.as_view('logout_view')
reset_password_view = Reset_passwordView.as_view('reset_password_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])

# Define the rule for the login url --->  /auth/login
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/login',
    view_func=login_view,
    methods=['POST'])

# Define the rule for the logout url --->  /auth/logout
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/logout',
    view_func=logout_view,
    methods=['POST'])

# Define the rule for the reset password url --->  /auth/reset-password
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/reset-password',
    view_func=reset_password_view,
    methods=['POST'])