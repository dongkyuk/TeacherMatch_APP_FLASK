from datetime import datetime
from flask import g
from sqlalchemy.dialects import mysql
from app.database import db


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

    def is_active(self):
        return True

    def get_id(self):
        return self.id

    def is_authenticated(self):
        return self.authenticated

    def is_anonymous(self):
        return False

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class Hashtag(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    content = db.Column(db.String(length=80))


class UserHashtag(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    user_id = db.Column(db.String)
    hashtag_id = db.Column(db.String)
    userType = db.Column(db.Enum('student', 'mentor', 'admin'))


class Heart(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    user_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)
    used = db.Column(db.Boolean)


class UnlockedProfile(db.Model):
    heart_id = db.Column(db.String, primary_key=True)
    student_id = db.Column(db.String(length=80))
    mentor_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)


class Match(db.Model):
    id = db.Column(db.String, unique=True, primary_key=True)
    heart_id = db.Column(db.String)
    student_id = db.Column(db.String(length=80))
    mentor_id = db.Column(db.String(length=80))
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)


class Mock_class_request(db.Model):
    match_id = db.Column(db.String, primary_key=True)
    timestamp = db.Column(db.DateTime)
    fulfilled = db.Column(db.Boolean)
