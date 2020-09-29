from flask import Flask, jsonify, request
from flask_restful import Api
from app.database import db
from app.UserHandler import login_manager, Register
# from app.UserHandler import

# Create/returns flask app with db
def create_app():
    # Create a flask app.
    app = Flask(__name__)
    # Set Config
    app.config.from_pyfile('config.py')
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

    ## Setup Api resource routing
    api.add_resource(Register, '/auth/register')

    # Run app
    app.run(port=5000, debug=True, host='localhost', use_reloader=True)

if __name__ == '__main__':
    main()
