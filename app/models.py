from datetime import datetime
from flask import g
from sqlalchemy.dialects import mysql
try:
    from database import db
    from auth import jwt, auth
except ImportError:
    from .database import db


class User(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'users'
    id = db.Column(db.String, unique=True, primary_key=True)
    password = db.Column(db.String(length=80))
    email = db.Column(db.String(length=80))
    name = db.Column(db.String(length=80))
    userType = db.Column(db.Enum('student', 'mentor', 'admin'))
    phone = db.Column(db.String(length=80))
    birthday = db.Column(db.DateTime)
    location = db.Column(db.String)
    # Other data
    data = db.Column(db.JSON)
    
    '''
    # Generates auth token.
    def generate_auth_token(self, permission_level):
        # Check if admin.
        if permission_level == 1:
            # Generate admin token with flag 1.
            token = jwt.dumps({'email': self.email, 'admin': 1})
            # Return admin flag.
            return token
        # Return normal user flag.
        return jwt.dumps({'email': self.email, 'admin': 0})

    # Generates a new access token from refresh token.
    @staticmethod
    @auth.verify_token
    def verify_auth_token(token):
        # Create a global none user.
        g.user = None

        try:
            # Load token.
            data = jwt.loads(token)

        except:
            # If any error return false.
            return False

        # Check if email and admin permission variables are in jwt.
        if 'email' and 'admin' in data:

            # Set email from jwt.
            g.user = data['email']

            # Set admin permission from jwt.
            g.admin = data['admin']

            # Return true.
            return True

        # If does not verified, return false.
        return False
    '''
    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def __repr__(self):
        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', type='%s', phone='%s', birthday='%s', location = '%s', data = '%s')>" % (
            self.id, self.username, self.password, self.email, self.created)

'''
class Hashtag_Following(db.Model):
    user_id = db.Column(db.String)
    hashtag_id = db.Column(db.String(length=80))
    content = db.Column(db.String(length=80))


class Hashtag_User(db.Model):
    user_id = db.Column(db.String)
    hashtag_id = db.Column(db.String(length=80))
    content = db.Column(db.String(length=80))

'''
class Heart(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    user_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)
    used = db.Column(db.Boolean)


class Unlocked_Profile(db.Model):
    heart_id = db.Column(db.String)
    student_id = db.Column(db.String(length=80))
    mentor_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)


class match(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    heart_id = db.Column(db.String)
    student_id = db.Column(db.String(length=80))
    mentor_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)


class mock_class_request(db.Model):
    match_id = db.Column(db.String)
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)
