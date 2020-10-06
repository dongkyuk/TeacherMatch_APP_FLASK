import bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import request, jsonify
from flask import current_app as app
from flask_restful import Resource
from password_validator import PasswordValidator

try:
    from messages import Message
    from models import User
    from database import db
except ImportError:
    from .messages import Message
    from .models import User
    from .database import db

# Init custom message
message = Message()

# Init login manager
login_manager = LoginManager()


# Create a schema
schema = PasswordValidator()
# Add properties to it
schema\
    .min(8)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()\



@login_manager.unauthorized_handler
def unauthorized():
    message.set_data({"login": "Login is required"})
    return message.UNAUTHORIZED


# user loader for login manager


@login_manager.user_loader
def user_loader(id):
    # Get user
    user = User.query.filter_by(id=id).first()

    return user

# Register new user


def password_hasher(password):
    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt())
    # Decode and return
    return hashed_password.decode('utf-8')


class Register(Resource):
    def post(self):
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

            # Get password
            org_password = json_data['password']
            # Check Schema
            if not schema.validate(org_password):
                message.set_data(
                    {"password": "Password does not match schema"})
                return message.INVALID_INPUT_422
            # Hash
            password = password_hasher(org_password)

        except Exception as why:
            # Log input strip or etc. messages.
            app.logger.info(str(why))
            # Return invalid input messages
            message.set_data({"user": "Given user info is wrong format"})
            return message.INVALID_INPUT_422

        # Check if any field is none.
        userInfo = [id, password, email, name,
                    userType, phone, birthday, location, data]

        for info in userInfo:
            if info is None:
                message.set_data({"user": "Given None for user data"})
                return message.INVALID_INPUT_422

        # Check if user existed.
        if user_loader(id) is not None:
            message.set_data({"user": "User already exists"})
            return message.ALREADY_EXIST

        # Create a new user.
        user = User(id=id, password=password, email=email, name=name,
                    userType=userType, phone=phone, birthday=birthday, location=location, data=data)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        message.set_data(None)
        return message.SUCCESS

# Login


class Login(Resource):
    def post(self):
        try:
            # Get user infos
            json_data = request.get_json()
            email = json_data['email']
            password = json_data['password']
        except Exception as why:
            # Log input strip or etc. messages.
            app.logger.info("Email or password is wrong. " + str(why))
            # Return invalid input message.
            message.set_data(
                {"user": "Given email or password is wrong format"})
            return message.INVALID_INPUT_422

        user = User.query.filter_by(email=email).first()

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            user.authenticated = True
            login_user(user, remember=True)

            message.set_data(None)
            return message.SUCCESS
        else:
            message.set_data({"password": "Password is wrong"})
            return message.INVALID_INPUT_422


class Logout(Resource):
    @login_required
    def post(self):
        user = current_user
        user.authenticated = False
        logout_user()
        message.set_data(None)
        return message.SUCCESS


class ResetPassword(Resource):
    @login_required
    def post(self):
        # Get old and new passwords.
        try:
            old_pass, new_pass = request.json.get(
                'old_pass'), request.json.get('new_pass')
        except Exception as why:
            # Log input strip or etc. messages.
            app.logger.info("Given Data is wrong. " + str(why))
            # Return invalid input messages
            message.set_data({"password": "Given passwords are wrong format"})
            return message.INVALID_INPUT_422

        # Get current user
        user = current_user
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


class UserData(Resource):
    @login_required
    def get(self):
        return current_user.__repr__()
