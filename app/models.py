from datetime import datetime
from flask import g
from sqlalchemy.dialects import mysql
from . import db


class User(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.VarChar, unique=True, primary_key=True)
    # User name.
    name = db.Column(db.String(length=80))
    # User type
    type = db.Column(db.Enum('student', 'mentor', 'admin'))
    # User phone.
    phone = db.Column(db.String(length=80))
    # User email address.
    birthday = db.Column(db.DateTime)
    # Creation time for user.
    location = db.Column(db.String)
    # Unless otherwise stated default role is user.
    data = db.Column(db.JSON)

    def __repr__(self):
        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', type='%s', phone='%s', birthday='%s', location = '%s', data = '%s')>" % (
            self.id, self.username, self.password, self.email, self.created)


class Login(db.Model):
    # User id.
    userID = db.Column(db.VarChar)
    # User name.
    password = db.Column(db.VarChar(length=80))
    # User email address.
    email = db.Column(db.VarChar(length=80))


class Hashtag_Following(db.Model):
    # User id.
    userID = db.Column(db.VarChar)
    # User name.
    hashtag_id = db.Column(db.VarChar(length=80))
    # User email address.
    email = db.Column(db.VarChar(length=80))


class Hashtag_User(db.Model):
    # User id.
    userID = db.Column(db.VarChar)
    # User name.
    hashtag_id = db.Column(db.VarChar(length=80))
    # User email address.
    content = db.Column(db.VarChar(length=80))


class Heart(db.Model):
    # User id.
    id = db.Column(db.VarChar, unique=True, primary_key=True)
    # User name.
    userID = db.Column(db.VarChar(length=80))
    # User email address.
    timestamp = db.Column(db.DateTime)
    used = db.Column(db.Boolean)


class Unlocked_Profile(db.Model):
    # User id.
    heartId = db.Column(db.VarChar)
    # User name.
    studentID = db.Column(db.VarChar(length=80))
    # User email address.
    mentorID = db.Column(db.VarChar(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)


class Match_Request(db.Model):
    # User id.
    id = db.Column(db.VarChar, unique=True, primary_key=True)
    heartId = db.Column(db.VarChar)
    # User name.
    studentID = db.Column(db.VarChar(length=80))
    # User email address.
    mentorID = db.Column(db.VarChar(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)
    
class Match_Request(db.Model):
    # User id.
    matchID = db.Column(db.VarChar)
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)

