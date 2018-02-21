from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

    #handle post request for this view( url is auth/register)
    def post(self):

        #get the json data sent over post as a dictionary
        data = request.get_json()

        # Query to see if the user already exists
        user = User.get_by_username(username=data['username'])

    

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')

# Define the rule for the registration url --->  /auth/register
# Then add the rule to the blueprint
auth_blueprint.add_url_rule(
    '/auth/register',
    view_func=registration_view,
    methods=['POST'])