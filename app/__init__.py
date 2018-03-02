from flask import Flask, current_app, session
from flask_sqlalchemy import SQLAlchemy
from config import config
from flasgger import Swagger, swag_from
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)
    
    #initialise app to use swagger for doc strings
    swagger = Swagger(app)

    #get configuration settings to app
    app.config.from_object(config[config_name])

    #apply the configuration settings on app
    config[config_name].init_app(app)

    #initialise sqlalchemy with setting in the app
    db.init_app(app)

    #No need for these imports since routes now in
    #blueprints
    from flask import request, jsonify, make_response



    # import the authentication blueprint and register it on the app
    from .api.v1.auth import auth_blueprint
    app.register_blueprint(auth_blueprint)

    # import the businesses blueprint and register it on the app
    from .api.v1.businesses import businesses_blueprint
    app.register_blueprint(businesses_blueprint)

    # import the reviews blueprint and register it on the app
    from .api.v1.reviews import reviews_blueprint
    app.register_blueprint(reviews_blueprint)

    return app