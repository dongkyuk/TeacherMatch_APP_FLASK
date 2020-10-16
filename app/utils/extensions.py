import bcrypt
from functools import wraps
from flask import abort
from flask_login import LoginManager, current_user
from password_validator import PasswordValidator
from app.models import User
from app.messages import Message

message = Message()

# Init and config login manager
login_manager = LoginManager()


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


# Create a password schema
schema = PasswordValidator()
schema\
    .min(8)\
    .max(100)\
    .has().uppercase()\
    .has().lowercase()\
    .has().digits()\
    .has().no().spaces()\



def type_required(type):
    # Decorator to check if user is certain type
    def type_required_sub(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if not current_user.userType is type:
                message.set_data({"user": "User does not have access"})
                return message.FORBIDDEN
            return func(*args, **kwargs)
        return wrapper
    return type_required_sub


def get_user(user_id):
    # Function to get and check user based on id
    if user_id == current_user.id:
        return current_user
    else:
        message.set_data({"user": "User does not have access"})
        abort(message.FORBIDDEN)


def password_hasher(password):
    # Hash password
    hashed_password = bcrypt.hashpw(
        password.encode('utf-8'), bcrypt.gensalt())
    # Decode and return
    return hashed_password.decode('utf-8')


def check_hashed_password(password1, password2):
    # Check if user password does not match with old password.
    return bcrypt.checkpw(password1.encode('utf-8'), password2.encode('utf-8'))
