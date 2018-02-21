from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

    #handle post request for this view( url is auth/register)
    def post(self):

        #get the json data sent over post as a dictionary
        try:
            data = request.get_json()
        except Exception as e:
            #check if nothing in json request
            if str(e) == "400 Bad Request: Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)":
                response = {
                    "message": "Please supply both username and password keys"
                }
                return make_response(jsonify(response)), 400
            if str(e) == "400 Bad Request: Failed to decode JSON object: Expecting ',' delimiter: line 3 column 2 (char 19)":
                response = {
                    "message": "Please supply both username and password values"
                }
                return make_response(jsonify(response)), 400
            response = {
                "message": str(e)
            }
            return make_response(jsonify(response)), 400
        
        #ensure that a username and password are provided
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
        user = User.get_by_username(username=data['username'])

        if not user:
            #user does not exist
            try:
                # Register the user
                username = data['username']
                password = data['password']
                user = User(username=username, password=password)
                User.add(user)

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
    def post(self):
        #Handle POST request for this view. Url ---> /auth/login
        """Endpoint to login a user"""
        try:

            #get the json data sent over post as a dictionary
            data = request.get_json()

            # Get the user object using their user name
            user = User.get_by_username(username=data['username'])

            # Try to authenticate the found user using their password
            if user and user.check_password_is_valid(password=data['password']):
                #check if user is already logged in
                if user.check_already_logged_in():
                    response = {
                        'message': 'No need you are already logged in'
                    }
                    #make and send the response
                    return make_response(jsonify(response)), 303
                else:
                    user.login_user()

                #valid username and password so generate success message
                response = {
                    'message': 'You logged in successfully.'
                }
                #make and send the response
                return make_response(jsonify(response)), 200
            else:
                # User does not exist. Therefore, we return an error message
                response = {
                    'message': 'Invalid username, Please try again'
                }
                return make_response(jsonify(response)), 401

        except Exception as e:

            #check if nothing in json request
            if str(e) == "400 Bad Request: Failed to decode JSON object: Expecting value: line 1 column 1 (char 0)":
                response = {
                    "message": "Please supply both username and password"
                }
                return make_response(jsonify(response)), 400

            # Create a response containing an string error message
            # incase an exception occurs
            response = {
                'message': str(e)
            }

            # Return a server error using the HTTP Error Code 500 (Internal Server Error)
            return make_response(jsonify(response)), 500
    

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')
login_view = LoginView.as_view('login_view')

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