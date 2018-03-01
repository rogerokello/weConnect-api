from flask import Blueprint

# This instance of a Blueprint that represents the authentication blueprint
reviews_blueprint = Blueprint('reviews', __name__)

from . import views