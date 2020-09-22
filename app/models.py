from datetime import datetime
from flask import g
from sqlalchemy.dialects import mysql
from . import db
from auth import jwt, auth

class User(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'users'
    userID = db.Column(db.VarChar, unique=True, primary_key=True)
    password = db.Column(db.VarChar(length=80))
    email = db.Column(db.VarChar(length=80))
    name = db.Column(db.String(length=80))
    userType = db.Column(db.Enum('student', 'mentor', 'admin'))
    phone = db.Column(db.String(length=80))
    birthday = db.Column(db.DateTime)
    location = db.Column(db.String)
    # Other data
    data = db.Column(db.JSON)

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

    def __repr__(self):
        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', type='%s', phone='%s', birthday='%s', location = '%s', data = '%s')>" % (
            self.id, self.username, self.password, self.email, self.created)


class Hashtag_Following(db.Model):
    userID = db.Column(db.VarChar)
    hashtag_id = db.Column(db.VarChar(length=80))
    email = db.Column(db.VarChar(length=80))


class Hashtag_User(db.Model):
    userID = db.Column(db.VarChar)
    hashtag_id = db.Column(db.VarChar(length=80))
    content = db.Column(db.VarChar(length=80))


class Heart(db.Model):
    heartId = db.Column(db.VarChar, unique=True, primary_key=True)
    userID = db.Column(db.VarChar(length=80))
    timestamp = db.Column(db.DateTime)
    used = db.Column(db.Boolean)


class Unlocked_Profile(db.Model):
    heartId = db.Column(db.VarChar)
    studentID = db.Column(db.VarChar(length=80))
    mentorID = db.Column(db.VarChar(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)


class Match_Request(db.Model):
    matchID = db.Column(db.VarChar, unique=True, primary_key=True)
    heartId = db.Column(db.VarChar)
    studentID = db.Column(db.VarChar(length=80))
    mentorID = db.Column(db.VarChar(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)


class mock_class_request(db.Model):
    matchID = db.Column(db.VarChar)
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)
