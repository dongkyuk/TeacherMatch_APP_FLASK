import bcrypt
import json
from functools import wraps
from flasgger import swag_from
from flask_login import LoginManager, login_user, logout_user, current_user, login_required, fresh_login_required
from flask import request, jsonify, abort
from flask import current_app as app
from flask_restful import Resource
from password_validator import PasswordValidator
from app.messages import Message
from app.models import User
from app.database import db


# Init custom message
message = Message()

# Init login manager
login_manager = LoginManager()

# Create a password schema
schema = PasswordValidator()
schema\
    .min(8)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()\



def get_user(user_id):
    # Function to get and check user based on id
    if user_id == current_user.id:
        return current_user
    else:
        message.set_data({"user": "User does not have access"})
        abort(message.FORBIDDEN)


def type_required(type):
    # Decorator to check if user is certain type
    def type_required_sub(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.userType == type:
                return type
                return current_user.userType
                message.set_data({"user": "User does not have access"})
                return message.FORBIDDEN
            return func(*args, **kwargs)
        return wrapper
    return type_required_sub


@login_manager.unauthorized_handler
def unauthorized():
    # Handle message when unauthorized
    message.set_data({"login": "Login is required"})
    return message.UNAUTHORIZED


@login_manager.user_loader
def user_loader(id):
    # user loader for login manager
    user = User.query.filter_by(id=id).first()
    return user


def password_hasher(password):
    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt())
    # Decode and return
    return hashed_password.decode('utf-8')


class Register(Resource):
    def post(self):
        # Register new user
        try:
            # Get user infos
            json_data = request.get_json()
            id = json_data['id']
            email = json_data['email']
            name = json_data['name']
            userType = json_data['userType']
            phone = json_data['phone']
            birthday = json_data['birthday']
            location = json_data['location']
            data = json_data['data']

            # Get original password
            org_password = json_data['password']

            # Check Schema
            if not schema.validate(org_password):
                message.set_data(
                    {"password": "Password does not match schema"})
                return message.INVALID_INPUT_422

            # Hash and save
            password = password_hasher(org_password)

        except Exception as why:
            app.logger.info(str(why))
            # Error message
            message.set_data({"user": "Given user info is wrong format"})
            return message.INVALID_INPUT_422

        userInfo = [id, password, email, name,
                    userType, phone, birthday, location, data]

        # Check if any field is none.
        for info in userInfo:
            if info is None:
                message.set_data({"user": "Given None for user data"})
                return message.INVALID_INPUT_422

        # Check if user existed.
        if user_loader(id) is not None:
            message.set_data({"user": "User already exists"})
            return message.ALREADY_EXIST

        # Create a new user instance
        user = User(id=id, password=password, email=email, name=name,
                    userType=userType, phone=phone, birthday=birthday, location=location, data=data)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        # Success message
        message.set_data(None)
        return message.SUCCESS


class Login(Resource):
    def post(self):
        try:
            # Get email and password
            json_data = request.get_json()
            id = json_data['id']
            email = json_data['email']
            password = json_data['password']
        except Exception as why:
            app.logger.info("Email or password is wrong. " + str(why))
            # Error message
            message.set_data(
                {"user": "Given email or password is wrong format"})
            return message.INVALID_INPUT_422

        # Get user from id or email
        user = user_loader(id)
        if user is None:
            user = User.query.filter_by(email=email).first()

        # Check if user exist
        if user is None:
            message.set_data(
                {"user": "No such user"})
            return message.DOES_NOT_EXIST

        # Check password
        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user.authenticated = True
            login_user(user, remember=True)
            # Success
            message.set_data(None)
            return message.SUCCESS
        else:
            # Error message
            message.set_data({"password": "Password is wrong"})
            return message.INVALID_INPUT_422


class Logout(Resource):
    @login_required
    def post(self, user_id):
        user = get_user(user_id)
        user.authenticated = False
        logout_user()

        message.set_data(None)
        return message.SUCCESS


class UserData(Resource):
    @login_required
    def get(self, user_id):
        # Get all user data
        user = get_user(user_id)
        return json.dumps(user.as_dict(), default=str)

    @login_required
    def post(self, user_id):
        # Change user info

        user = get_user(user_id)

        try:
            # Get user infos
            json_data = request.get_json()
            email = json_data['email']
            name = json_data['name']
            phone = json_data['phone']
            birthday = json_data['birthday']
            location = json_data['location']
            data = json_data['data']

        except Exception as why:
            # Log
            app.logger.info(str(why))
            # Error message
            message.set_data({"user": "Given user info is wrong format"})
            return message.INVALID_INPUT_422

        # Check if any field is none.
        userInfo = [id, email, name, phone, birthday, location, data]

        for info in userInfo:
            if info is None:
                message.set_data({"user": "Given None for user data"})
                return message.INVALID_INPUT_422

        # Update info
        user.email = email
        user.name = name
        user.phone = phone
        user.birthday = birthday
        user.location = location
        user.data = data

        # Commit session.
        db.session.commit()

        # Success message
        message.set_data(None)
        return message.SUCCESS


class Password(Resource):
    @login_required
    @fresh_login_required
    def post(self, user_id):
        # Change password

        user = get_user(user_id)

        try:
            # Get old and new passwords.
            json_data = request.get_json()
            old_pass = json_data['old_pass']
            new_pass = json_data['new_pass']
        except Exception as why:
            # Log
            app.logger.info(str(why))
            # Error message
            message.set_data(
                {"password": "Given password info is wrong format"})
            return message.INVALID_INPUT_422

        # Check if user password does not match with old password.
        if not bcrypt.checkpw(old_pass.encode('utf-8'), user.password.encode('utf-8')):
            # Return does not match status.
            message.set_data({"password": "Password is wrong"})
            return message.INVALID_INPUT_422

        # Update password.
        user.password = password_hasher(new_pass)

        # Commit session.
        db.session.commit()

        # Return success status.
        message.set_data(None)
        return message.SUCCESS
