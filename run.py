import logging
from flasgger import Swagger
from flask import Flask
from flask_restful import Api
from app.database import db
from app.UserHandler import login_manager, Register, Login, Logout, UserData
from app.MatchHandler import Hearts, Matches, Hashtags, UserHashtags
# from app.UserHandler import

# Create/returns flask app with db


def create_app():
    # Create a flask app.
    app = Flask(__name__)
    # Set Config
    app.config.from_pyfile('config.py')
    logging.basicConfig(level=logging.INFO)
    # Return app.
    return app


def db_config(app):
    db.init_app(app)


def login_config(app):
    login_manager.init_app(app)

# Create/returns api with given app


def create_api(app):
    # Initialize API
    api = Api(app)
    # Return api
    return api


def main():
    # Make app, configure db,login and make api
    app = create_app()
    db_config(app)
    login_config(app)
    api = Api(app)

    # Swagger for documentation
    swagger = Swagger(app)

    # Setup Api resource routing
    api.add_resource(Register, '/register')
    api.add_resource(Login, '/login')
    api.add_resource(Logout, '/users/<string:user_id>/logout')
#    api.add_resource(ResetPassword, '/user/<string:id>/password')
    api.add_resource(UserData, '/users/<string:user_id>/data')

    api.add_resource(Hearts, '/users/<string:user_id>/heart')
    api.add_resource(Matches, '/users/<string:user_id>/match')
    api.add_resource(Hashtags, '/hashtags')
    api.add_resource(UserHashtags, '/users/<string:user_id>/hashtag')
    # Run app
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)


if __name__ == '__main__':
    main()
