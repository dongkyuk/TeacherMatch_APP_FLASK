from datetime import datetime
from flask import g
from sqlalchemy.dialects import mysql
from . import db

class User(db.Model):
    # Generates default class name for table. For changing use
    # __tablename__ = 'users'

    # User id.
    id = db.Column(db.VarChar, primary_key=True)
    # User name.
    name = db.Column(db.String(length=80))
    # User type
    type = db.Column(db.Enum('student', 'mentor', 'admin'))
    # User phone.
    phone = db.Column(db.String(length=80))
    # User email address.
    birthday = db.Column(db.DateTime)
    # Creation time for user.
    location = db.Column(db.DateTime)
    # Unless otherwise stated default role is user.
    data = db.Column(db.JSON)

    def __repr__(self):
        # This is only for representation how you want to see user information after query.
        return "<User(id='%s', name='%s', type='%s', phone='%s', birthday='%s', location = '%s', data = '%s')>" % (
                      self.id, self.username, self.password, self.email, self.created)