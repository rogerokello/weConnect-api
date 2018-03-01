from app import db, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta
#from .user import User
#from app.v1.models.loggedinuser import Loggedinuser
#from app.v1.models.business import Business
#from v1.models.review import Review

class Business(db.Model): 
    __tablename__ = 'businesses'
    #the fields of the Business table
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    category = db.Column(db.String(64))
    location = db.Column(db.String(64))
    #user_id = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='creator', lazy='dynamic')


    def add(self):
        db.session.add(self)
        db.session.commit()
