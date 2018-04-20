from app import db, current_app
from flask_bcrypt import Bcrypt
import jwt
from datetime import datetime, timedelta


class Business(db.Model): 
    __tablename__ = 'businesses'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    category = db.Column(db.String(64))
    location = db.Column(db.String(64))
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='business', lazy='dynamic', cascade='all, delete-orphan')


    def add(self):
        db.session.add(self)
        db.session.commit()
