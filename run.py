import os
from flask import Flask, jsonify, request
from flask_restful import Api
from sqlalchemy import create_engine, text
from api.handlers.UserHandlers import (AddUser, DataAdminRequired,
                                       DataUserRequired, Login, Logout,
                                       RefreshToken, Register, ResetPassword,
                                       UsersData)
def create_app():
    # Create a flask app.
    app = Flask(__name__)
    # Set Config
    app.config.from_pyfile('config.py')
    # Set debug true for catching the errors.
    app.config['TESTING'] = True
    #  Database initialize
    db = create_engine(app.config['DB_URL'], encoding = 'utf-8')
    app.database = db

    # Return app.
    return app


if __name__ == '__main__':
    # Create app.
    app = create_app()

    # Add resource classes
    api = Api(app)
    api.add_resource(Register, '/v1/auth/register')
    api.add_resource(Login, '/v1/auth/login')
    api.add_resource(Logout, '/v1/auth/logout')
    api.add_resource(RefreshToken, '/v1/auth/refresh')
    api.add_resource(ResetPassword, '/v1/auth/password_reset')
    api.add_resource(UsersData, '/users')
    api.add_resource(DataAdminRequired, '/data_admin')
    api.add_resource(DataUserRequired, '/data_user')
    api.add_resource(AddUser, '/user_add')

    # Run app.
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)
