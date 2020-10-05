import logging
import uuid
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import g, request, jsonify
from flask_restful import Resource

try:
    from errors import Error
    from models import Heart, Match
    from database import db
except ImportError:
    from .errors import Error
    from .models import Heart, Match
    from .database import db

# Init custom error
error = Error()

# Load heart with id


def heart_loader(id):
    # Get heart
    heart = Heart.query.filter_by(id=id).first()
    return heart


# Load match with id
def match_loader(id):
    # Get match
    match = Match.query.filter_by(id=id).first()
    return match


# Make heart when given timestamp


class Heart(Resource):
    @staticmethod
    @login_required()
    def post():
        try:
            json_data = request.get_json()
            timestamp = json_data['timestamp']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            return error.INVALID_INPUT_422

        # Get current user id
        user_id = current_user.id

        # Create random heart id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(heart_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new heart
        heart = Heart(id=id, user_id=user_id, timestamp=timestamp, used=False)

        # Add heart to session.
        db.session.add(heart)

        # Commit session.
        db.session.commit()

        return {'status': 'heart creation completed.'}

    def put():
        try:
            json_data = request.get_json()
            user_id = json_data['user_id']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            return error.INVALID_INPUT_422

        # Find Usable Heart
        heart = Heart.query.filter_by(user_id=user_id).first()
        if heart is None:
            return "No available heart!"
        if heart["used"]:
            while():
                return "All hearts are used!"


class Match(Resource):
    @staticmethod
    @login_required()
    def post():
        try:
            json_data = request.get_json()
            mentor_id = json_data['mentor_id']
            timestamp = json_data['timestamp']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            return error.INVALID_INPUT_422

        # Get current student id
        if current_user.userType == "student":
            student_id = current_user.id
        else:
            return "Only students can request match"

        Heart.put()

        # Create random match id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(match_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new match
        match = Match(id=id, heart_id=heart.id, student_id=student_id,
                      mentor_id=mentor_id, timestamp=timestamp, fulfilled=False)

        # Add match to session.
        db.session.add(match)

        # Commit session.
        db.session.commit()

        return {'status': 'match creation completed.'}

    def put():
        try:
            json_data = request.get_json()
            mentor_id = json_data['mentor_id']
            timestamp = json_data['timestamp']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            return error.INVALID_INPUT_422

        # Get current student id
        if current_user.userType == "mentor":
            mentor_id = current_user.id
        else:
            return "Only mentors can request match"

        # Find usable heart
        Heart.put()

        # Create a new match
        match = Match(id=id, heart_id=heart.id, student_id=student_id,
                      mentor_id=mentor_id, timestamp=timestamp, fulfilled=False)

        # Add match to session.
        db.session.add(match)

        # Commit session.
        db.session.commit()

        return {'status': 'match creation completed.'}


