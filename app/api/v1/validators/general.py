from functools import wraps
from flask import request, jsonify, make_response
from app.models.user import User


def validate(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # get authorisation header
        auth_header = request.headers.get('Authorization')

        if auth_header is None:
            return make_response(jsonify(
                    {
                        "Header Error": " Please provide an Authorisation header",
                        "status": "failure"
                    }
            )), 403

        if isinstance(auth_header, str) is not True:
            return make_response(jsonify(
                    {
                        "Header Error": " Please use an Authorization header that is a string",
                        "status": "failure"
                    }
            )), 403


        auth_token = None

        if len(auth_header.split(" ")) == 1:
            return make_response(jsonify(
                        {
                            "Token Error": " Token not being sent in the right format ",
                            "status": "failure"
                        }
            )), 403

        #pick token after splitting with the bearer
        if len(auth_header.split(" ")) > 1:
            auth_token = auth_header.split(" ")[1]

        if auth_token is None:
            return make_response(jsonify(
                    {
                        "Token Error": "Token required",
                        "status": "failure"
                    }
            )), 403
            
        #decode the token that was stored after login to extract the user id
        user_id = User.get_token_user_id(auth_token)

        if user_id == "Expired token. Please login to get a new token":
            return make_response(jsonify(
                            {
                                "Token Error": " Token Expired. Please login to get a new one",
                                "status": "failure"
                            }
                    )), 403

        if user_id == "Invalid token. Please register or login":
            return make_response(jsonify(
                            {
                                "Token Error": " Invalid Token. Please login to get a new one",
                                "status": "failure"
                            }
                    )), 403
        
        return f(*args, **kwargs)
    return decorated_function