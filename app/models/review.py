from app import db, current_app
from flask_bcrypt import Bcrypt
import jwt


class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    review_summary = db.Column(db.String(64))
    review_description = db.Column(db.String(150))
    star_rating = db.Column(db.String(10))
    date_created = db.Column(
        db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(
        db.DateTime, default=db.func.current_timestamp(),
        onupdate=db.func.current_timestamp())
    business_id = db.Column(db.Integer, db.ForeignKey('businesses.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    #save the review
    def save(self):
        db.session.add(self)
        db.session.commit()