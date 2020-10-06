import logging
import uuid
from flask_login import LoginManager, login_user, logout_user, current_user, login_required
from flask import g, request, jsonify
from flask_restful import Resource

try:
    from messages import Message
    from models import User, Hashtag, UserHashtag, Heart, UnlockedProfile, Match, Mock_class_request
    from database import db
except ImportError:
    from .messages import Message
    from .models import User, Hashtag, UserHashtag, Heart, UnlockedProfile, Match, Mock_class_request
    from .database import db

# Init custom error
message = Message()

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

# Load hashtag with id


def hashtag_loader(id):
    # Get match
    hashtag = Hashtag.query.filter_by(id=id).first()
    return hashtag

# Make heart when given timestamp


class Hearts(Resource):
    @login_required
    def get(self):
        # Get current user id
        user_id = current_user.id

        # Get first heart
        heart = Heart.query.filter_by(user_id=user_id, used=False).first()

        if heart is None:
            message.set_data({"id": None})
        else:
            message.set_data({"id": heart.id})

        return message.SUCCESS

    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            timestamp = json_data['timestamp']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"timestamp": "Given Timestamp is wrong format"})
            return message.INVALID_INPUT_422

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

        message.set_data({'heart_id': heart.id})
        return message.SUCCESS

    @login_required
    def put(self):
        # Find Usable Heart
        heart_json = Hearts.get(self)

        id = heart_json[0]["data"]["id"]
        if id is None:
            message.set_data({"heart": "No usable heart exists"})
            return message.DOES_NOT_EXIST
        else:
            heart = heart_loader(id)

        heart.used = True

        # Commit session.
        db.session.commit()

        message.set_data({"id": id})
        return message.SUCCESS


class Matches(Resource):
    @login_required
    def get(self):
        # Get current user id
        user_id = current_user.id
        # Get first heart
        if current_user.userType == "student":
            match = Match.query.filter_by(student_id=user_id).first()
        elif current_user.userType == "mentor":
            match = Match.query.filter_by(mentor_id=user_id).first()

        if match is None:
            message.set_data({"id": None})
        else:
            message.set_data({"id": match.id})

        return message.SUCCESS

    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            mentor_id = json_data['mentor_id']
            timestamp = json_data['timestamp']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"match": "Given match data is wrong format"})
            return message.INVALID_INPUT_422

        # Get current student id
        if current_user.userType == "student":
            student_id = current_user.id
        else:
            message.set_data({"auth": "Only students can request match"})
            return message.FORBIDDEN

        # Check if existing mentor
        if User.query.filter_by(id=mentor_id).first() is None:
            message.set_data({"mentor_id": "Mentor does not exist"})
            return message.NOT_FOUND_404

        heart_json = Hearts.put(Resource)
        if heart_json[1] != 200:
            return heart_json
        heart_id = heart_json[0]['data']['id']

        # Create random match id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(match_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new match
        match = Match(id=id, heart_id=heart_id, student_id=student_id,
                      mentor_id=mentor_id, timestamp=timestamp, fulfilled=False)

        # Add match to session.
        db.session.add(match)

        # Commit session.
        db.session.commit()

        message.set_data({"id": match.id})
        return message.SUCCESS


class Hashtags(Resource):
    @login_required
    def get(self):
        # Get all hashtags
        hashtags = Hashtag.query.all()

        if hashtags is None:
            message.set_data({"id_lst": None, "content_lst": None})
        else:
            message.set_data(
                {"id_lst": [hashtag.id for hashtag in hashtags], "content_lst": [hashtag.content for hashtag in hashtags]})

        return message.SUCCESS

    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            content = json_data["content"]
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"match": "Given content data is wrong format"})
            return message.INVALID_INPUT_422

        # Check if existing content
        if Hashtag.query.filter_by(content=content).first() is not None:
            message.set_data({"content": "Already existing hashtag"})
            return message.ALREADY_EXIST

        # Create random hashtag id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(hashtag_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new hashtag
        hashtag = Hashtag(id=id, content=content)

        # Add match to session.
        db.session.add(hashtag)

        # Commit session.
        db.session.commit()

        message.set_data({"id": hashtag.id, "content": content})
        return message.SUCCESS


class UserHashtags(Resource):
    @login_required
    def get(self):
        # Get current user id
        user_id = current_user.id

        # Get first hashtag
        hashtags = UserHashtag.query.filter_by(user_id=user_id).all()

        if hashtags is None:
            message.set_data({"id_lst": None})
        else:
            message.set_data(
                {"id_lst": [hashtag.hashtag_id for hashtag in hashtags]})

        return message.SUCCESS

    @login_required
    def post(self):
        try:
            json_data = request.get_json()
            hashtag_id = json_data['hashtag_id']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))

            message.set_data(
                {"hashtag_id": "Given hashtag id is wrong format"})
            return message.INVALID_INPUT_422

        # Check if existing content
        if UserHashtag.query.filter_by(hashtag_id=hashtag_id).first() is not None:
            message.set_data({"hashtag_id": "Already following hashtag"})
            return message.ALREADY_EXIST

        # Create random hashtag id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(hashtag_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new hashtag
        user_hashtag = UserHashtag(
            id=id, hashtag_id=hashtag_id, user_id=current_user.id)

        # Add match to session.
        db.session.add(user_hashtag)

        # Commit session.
        db.session.commit()

        message.set_data({"id": user_hashtag.id})
        return message.SUCCESS

    @login_required
    def delete(self):
        try:
            json_data = request.get_json()
            hashtag_id = json_data['hashtag_id']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))

            message.set_data(
                {"hashtag_id": "Given hashtag id is wrong format"})
            return message.INVALID_INPUT_422

        user_hashtag = UserHashtag.query.filter_by(
            hashtag_id=hashtag_id, user_id=current_user.id).first()
        # Check if existing content
        if user_hashtag is None:
            message.set_data({"hashtag_id": "Not following hashtag"})
            return message.DOES_NOT_EXIST

        # Add match to session.
        db.session.delete(user_hashtag)

        # Commit session.
        db.session.commit()

        message.set_data(None)
        return message.SUCCESS
