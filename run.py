import logging
from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from app.database import db
from app.resources.UserHandler import login_manager, Register, Login, Logout, UserData, Password
from app.resources.MatchHandler import Hearts, Matches, Hashtags, UserHashtags, UserFeed, UnlockedProfiles


def create_app():
    # Create a flask app.
    app = Flask(__name__)
    # Set Config
    app.config.from_pyfile('config.py')
    logging.basicConfig(level=logging.INFO)
    # Return app.
    return app


def db_config(app):
    with app.app_context():
        db.init_app(app)
        db.create_all()


def create_api(app):
    # Initialize API
    api = Api(app)
    # Return api
    return api


def main():
    # Make app and configure db/login
    app = create_app()
    db_config(app)
    login_manager.init_app(app)
    api = Api(app)

    # Swagger for documentation
    swagger = Swagger(app)

    # Setup UserHandler api resource routing
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/users/<string:user_id>/logout')
    api.add_resource(Password, '/user/<string:user_id>/password')
    api.add_resource(UserData, '/users/<string:user_id>/data')

    # Setup UserHandler api resource routing
    api.add_resource(Hearts, '/users/<string:user_id>/heart')
    api.add_resource(Matches, '/users/<string:user_id>/match')
    api.add_resource(Hashtags, '/hashtags')
    api.add_resource(UserHashtags, '/users/<string:user_id>/hashtag')
    api.add_resource(UserFeed, '/users/<string:user_id>/feed')
    api.add_resource(UnlockedProfiles, '/users/<string:user_id>/unlockedprofile')

    # Run app
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)


if __name__ == '__main__':
    main()
