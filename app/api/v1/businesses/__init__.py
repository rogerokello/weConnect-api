from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
businesses_blueprint = Blueprint('businesses', __name__)

from . import views