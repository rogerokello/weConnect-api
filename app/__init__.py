from flask import Flask, current_app, session
#from . import db
from flask_sqlalchemy import SQLAlchemy
from config import config
from flasgger import Swagger, swag_from
db = SQLAlchemy()


def create_app(config_name):
    app = Flask(__name__)

    #make configuration for swagger
    app.config['SWAGGER'] = {
            'swagger': '2.0',
            'title': 'we-connect-you-api',
            'description': "The we-connect-you app allows you to register a business and\
            make reviews of other businesses",
            'basePath': '/app/v1/',
            'version': '0.0.1',
            'contact': {
                'Developer': 'Roger Okello',
                'email': 'rogerokello@gmail.com'
            },
            'license': {
                'name': 'MIT'
            },
            'tags': [
                {
                    'name': 'User',
                    'description': 'The user of the system'
                },
                {
                    'name': 'Business',
                    'description': 'Businesses that you can connect with to get\
                    a service'
                },
                {
                    'name': 'Review',
                    'description': 'A user rating and remarks for a business'
                },
            ]
        }
    
    #initialise app to use swagger for doc strings
    swagger = Swagger(app)

    #get configuration settings to app
    app.config.from_object(config[config_name])

    #apply the configuration settings on app
    config[config_name].init_app(app)

    #from app.v1.models.business import Business, Review, User, Loggedinuser
    from app.models.review import Review
    from app.models.user import User
    from app.models.loggedinuser import Loggedinuser
    db.init_app(app)
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