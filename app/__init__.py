from flask import Flask
from . import db

def create_app():
    app = Flask(__name__)
    from .models import Business
    
    return app