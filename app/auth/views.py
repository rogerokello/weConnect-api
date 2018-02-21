from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User

class RegistrationView(MethodView):
    """This class registers a new user."""

# Define the API resource
registration_view = RegistrationView.as_view('registration_view')