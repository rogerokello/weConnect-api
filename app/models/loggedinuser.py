from app import db, current_app
from flask_bcrypt import Bcrypt
import jwt

#from app.v1.models.user import User
#from app.v1.models.loggedinuser import Loggedinuser
#from app.v1.models.business import Business
#from app.v1.models.review import Review

class Loggedinuser(db.Model):
    __tablename__ = 'loggedinusers'
    #fields
    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.Text())


    #Create a class method to add the token
    def add(self):
       db.session.add(self)
       db.session.commit()

    @classmethod
    def delete_token(self, token):
        db.session.delete(token)
        db.session.commit()