from . import auth_blueprint

from flask.views import MethodView
from flask import make_response, request, jsonify
from app.models import User