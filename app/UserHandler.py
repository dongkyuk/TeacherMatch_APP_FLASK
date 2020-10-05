import logging
import bcrypt
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import g, request, jsonify
from flask_restful import Resource
from password_validator import PasswordValidator

try:
    from errors import Error
    from models import User
    from database import db
except ImportError:
    from .errors import Error
    from .models import User
    from .database import db


# Init login manager
login_manager = LoginManager()

# Init custom error
error = Error()

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


# user loader for login manager


@login_manager.user_loader
def user_loader(email):
    # Get user
    user = User.query.filter_by(email=email).first()

    return user

# Register new user


class Register(Resource):
    @staticmethod
    def post():
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
            if not schema.validate(org_password):
                logging.info("Wrong Password")
                return error.INVALID_INPUT_422
            # Hash password
            hashed_password = bcrypt.hashpw(
                org_password.encode('utf-8'), bcrypt.gensalt())
            # Decode and save
            password = hashed_password.decode('utf-8')

        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input error.s
            return error.INVALID_INPUT_422

        # Check if any field is none.
        userInfo = [id, password, email, name,
                    userType, phone, birthday, location, data]

        for info in userInfo:
            if info is None:
                return error.INVALID_INPUT_422

        # Check if user existed.
        if user_loader(email) is not None:
            return error.ALREADY_EXIST

        # Create a new user.
        user = User(id=id, password=password, email=email, name=name,
                    userType=userType, phone=phone, birthday=birthday, location=location, data=data)

        # Add user to session.
        db.session.add(user)

        # Commit session.
        db.session.commit()

        return {'status': 'registration completed.'}

# Login


class Login(Resource):
    @staticmethod
    def post():
        try:
            # Get user infos
            json_data = request.get_json()
            email = json_data['email']
            password = json_data['password']

        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Email or password is wrong. " + str(why))

            # Return invalid input error.
            return error.INVALID_INPUT_422

        user = user_loader(email)

        if bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            json_res = {'ok': True, 'msg': 'user <%s> logined' % id}
            user.authenticated = True
            login_user(user, remember=True)
        else:
            json_res = {'ok': False, 'error': 'Invalid user_id or password'}
        user = current_user
        return jsonify(json_res)


class Logout(Resource):
    @staticmethod
    @login_required
    def post():
        user = current_user
        user.authenticated = False
        json_res = {'ok': True, 'msg': 'user <%s> logout' % user.user_id}
        logout_user()
        return jsonify(json_res)


'''
        flask.flash('Logged in successfully.')

        next = flask.request.args.get('next')
        # is_safe_url should check if the url is safe for redirects.
        # See http://flask.pocoo.org/snippets/62/ for an example.
        if not is_safe_url(next):
            return flask.abort(400)

        return flask.redirect(next or flask.url_for('index'))
    return flask.render_template('login.html', form=form)

     if user.userType == 'student':
            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(0)
        # If user is mentor.
        elif user.userType == 'mentor':
            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 1 or 0.
            access_token = user.generate_auth_token(0)
        # If user is super admin.
        elif user.userType == 'admin':
            # Generate access token. This method takes boolean value for checking admin or normal user. Admin: 2, 1, 0.
            access_token = user.generate_auth_token(1)
        else:
            return error.INVALID_INPUT_422

        # Generate refresh token.
        refresh_token = refresh_jwt.dumps({'email': email})

        # Return access token and refresh token.
        return {'access_token': access_token.decode(), 'refresh_token': refresh_token.decode()}


class Logout(Resource):
    @staticmethod
    @auth.login_required
    def post():
        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        # Get if the refresh token is in blacklist
        ref = Blacklist.query.filter_by(refresh_token=refresh_token).first()

        # Check refresh token is existed.
        if ref is not None:
            return {'status': 'already invalidated', 'refresh_token': refresh_token}

        # Create a blacklist refresh token.
        blacklist_refresh_token = Blacklist(refresh_token=refresh_token)

        # Add refresh token to session.
        db.session.add(blacklist_refresh_token)

        # Commit session.
        db.session.commit()

        # Return status of refresh token.
        return {'status': 'invalidated', 'refresh_token': refresh_token}


class RefreshToken(Resource):
    @staticmethod
    def post():
        # Get refresh token.
        refresh_token = request.json.get('refresh_token')

        try:
            # Generate new token.
            data = refresh_jwt.loads(refresh_token)

        except Exception as why:
            # Log the error.
            logging.error(why)
            # If it does not generated return false.
            return False

        # Create user not to add db. For generating token.
        user = User(email=data['email'])

        # New token generate.
        token = user.generate_auth_token(False)

        # Return new access token.
        return {'access_token': token}


class ResetPassword(Resource):
    @auth.login_required
    def post(self):

        # Get old and new passwords.
        old_pass, new_pass = request.json.get(
            'old_pass'), request.json.get('new_pass')

        # Get user. g.user generates email address cause we put email address to g.user in models.py.
        user = User.query.filter_by(email=g.user).first()

        # Check if user password does not match with old password.
        if user.password != old_pass:

            # Return does not match status.
            return {'status': 'old password does not match.'}

        # Update password.
        user.password = new_pass

        # Commit session.
        db.session.commit()

        # Return success status.
        return {'status': 'password changed.'}


class UsersData(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        try:
            # Get usernames.
            usernames = [] if request.args.get(
                'usernames') is None else request.args.get('usernames').split(',')

            # Get emails.
            emails = [] if request.args.get(
                'emails') is None else request.args.get('emails').split(',')

            # Get start date.
            start_date = datetime.strptime(
                request.args.get('start_date'), '%d.%m.%Y')

            # Get end date.
            end_date = datetime.strptime(
                request.args.get('end_date'), '%d.%m.%Y')

            print(usernames, emails, start_date, end_date)

            # Filter users by usernames, emails and range of date.
            users = User.query\
                .filter(User.username.in_(usernames))\
                .filter(User.email.in_(emails))\
                .filter(User.created.between(start_date, end_date))\
                .all()

            # Create user schema for serializing.
            user_schema = UserSchema(many=True)

            # Get json data
            data, errors = user_schema.dump(users)

            # Return json data from db.
            return data

        except Exception as why:

            # Log the error.
            logging.error(why)

            # Return error.
            return error.INVALID_INPUT_422


# auth.login_required: Auth is necessary for this handler.
# role_required.permission: Role required user=0, admin=1 and super admin=2.

class DataAdminRequired(Resource):
    @auth.login_required
    @role_required.permission(1)
    def get(self):
        return "Test admin data OK."


class AddUser(Resource):
    @auth.login_required
    @role_required.permission(2)
    def get(self):
        return "OK"


class DataUserRequired(Resource):
    @auth.login_required
    def get(self):
        return "Test user data OK."
'''
