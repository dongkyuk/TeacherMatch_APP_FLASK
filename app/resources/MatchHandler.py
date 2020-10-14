import logging
import uuid
from flask_login import login_required, fresh_login_required
from flask import g, request, jsonify
from flask_restful import Resource
from app.messages import Message
from app.models import User, Hashtag, UserHashtag, Heart, UnlockedProfile, Match, Mock_class_request
from app.resources.UserHandler import login_manager, type_required, get_user
from app.database import db
from app.recommender import RecommenderModel

message = Message()  # Init custom error


def heart_loader(id):
    heart = Heart.query.filter_by(id=id).first()
    return heart


def match_loader(id):
    match = Match.query.filter_by(id=id).first()
    return match


def hashtag_loader(id):
    hashtag = Hashtag.query.filter_by(id=id).first()
    return hashtag


class Hearts(Resource):
    method_decorators = [login_required]

    def get(self, user_id):
        # Get an unused heart

        _ = get_user(user_id)

        heart = Heart.query.filter_by(user_id=user_id, used=False).first()

        if heart is None:
            message.set_data({"id": None})
        else:
            message.set_data({"id": heart.id})

        return message.SUCCESS

    def post(self, user_id):
        # Make heart when given timestamp

        _ = get_user(user_id)

        try:
            json_data = request.get_json()
            timestamp = json_data['timestamp']
        except Exception as why:
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"timestamp": "Given Timestamp is wrong format"})
            return message.INVALID_INPUT_422

        id = uuid.uuid1()  # Create random heart id
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

    def put(self, user_id):
        # Use Heart
        _ = get_user(user_id)

        # Find Usable Heart
        heart_json = Hearts.get(self, user_id)

        id = heart_json[0]["data"]["id"]
        if id is None:
            message.set_data({"heart": "No usable heart exists"})
            return message.DOES_NOT_EXIST
        else:
            heart = heart_loader(id)

        # Use Heart
        heart.used = True

        # Commit session.
        db.session.commit()

        message.set_data({"id": id})
        return message.SUCCESS


class UnlockedProfiles(Resource):
    method_decorators = [login_required]

    @type_required("student")
    def get(self, user_id):
        _ = get_user(user_id)
        '''
        under construction
        '''
        return None

    @type_required("student")
    def post(self, user_id):
        student_id = get_user(user_id)

        try:
            json_data = request.get_json()
            mentor_id = json_data['mentor_id']
            heart_id = json_data['heart_id']
            timestamp = json_data['timestamp']
        except Exception as why:
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"data": "Given data is wrong format"})
            return message.INVALID_INPUT_422

        # Create a new unlocked profile
        unlocked_prof = UnlockedProfile(
            heart_id=heart_id, student_id=student_id, mentor_id=mentor_id, timestamp=timestamp)

        # Add heart to session.
        db.session.add(unlocked_prof)

        # Commit session.
        db.session.commit(unlocked_prof)

        message.set_data({'heart_id': heart.id})
        return message.SUCCESS


class Matches(Resource):
    method_decorators = [login_required]

    def get(self, user_id):
        # Get all matches
        user = get_user(user_id)

        # Check user type
        if user.userType == "student":
            match_lst = Match.query.filter_by(student_id=user_id).all()
        elif user.userType == "mentor":
            match_lst = Match.query.filter_by(mentor_id=user_id).all()

        if match_lst is None:
            message.set_data({"id_lst": None})
        else:
            message.set_data({"id_lst": [match.id for match in match_lst]})

        return message.SUCCESS

    @type_required("student")
    def post(self, user_id):
        # Create match given mentor_id and timestamp
        _ = get_user(user_id)

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

        # Check if existing mentor
        if User.query.filter_by(id=mentor_id).first() is None:
            message.set_data({"mentor_id": "Mentor does not exist"})
            return message.NOT_FOUND_404

        # Use heart
        heart_json = Hearts.put(Resource, user_id)
        if heart_json[1] != 200:
            return heart_json
        heart_id = heart_json[0]['data']['id']

        # Create random match id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(match_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new match
        match = Match(id=id, heart_id=heart_id, student_id=user_id,
                      mentor_id=mentor_id, timestamp=timestamp, fulfilled=False)

        # Add match to session.
        db.session.add(match)

        # Commit session.
        db.session.commit()

        message.set_data({"id": match.id})
        return message.SUCCESS

    @type_required("mentor")
    def put(self, user_id):
        _ = get_user(user_id)
        try:
            json_data = request.get_json()
            match_id = json_data['match_id']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))
            # Return invalid input errors
            message.set_data({"match": "Given match id is wrong format"})
            return message.INVALID_INPUT_422

        # Check if existing match
        match = Match.query.filter_by(id=match_id).first()
        if match is None:
            message.set_data({"match_id": "Match does not exist"})
            return message.NOT_FOUND_404

        # Use Heart
        heart_json = Hearts.put(Resource, user_id)
        if heart_json[1] != 200:
            return heart_json

        # Fulfill match
        match.fulfilled = True

        # Commit session.
        db.session.commit()

        message.set_data({"id": match.id})
        return message.SUCCESS


class Hashtags(Resource):
    method_decorators = [login_required]

    def get(self):
        # Get all hashtags
        hashtags = Hashtag.query.all()

        if hashtags is None:
            message.set_data({"id_lst": None, "content_lst": None})
        else:
            message.set_data(
                {"id_lst": [hashtag.id for hashtag in hashtags], "content_lst": [hashtag.content for hashtag in hashtags]})

        return message.SUCCESS

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
    method_decorators = [login_required]

    def get(self, user_id):
        # Get all following hashtag
        _ = get_user(user_id)

        hashtags = UserHashtag.query.filter_by(user_id=user_id).all()

        if hashtags is None:
            message.set_data({"id_lst": None})
        else:
            message.set_data(
                {"id_lst": [hashtag.hashtag_id for hashtag in hashtags]})

        return message.SUCCESS

    def post(self, user_id):
        # Follow new hashtag
        user = get_user(user_id)

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
        if UserHashtag.query.filter_by(user_id=user_id, hashtag_id=hashtag_id).first() is not None:
            print(UserHashtag.query.filter_by(
                hashtag_id=hashtag_id).first().id)
            message.set_data({"hashtag_id": "Already following hashtag"})
            return message.ALREADY_EXIST

        # Create random hashtag id
        id = uuid.uuid1()
        # Repeat if id already exists
        while(hashtag_loader(id) is not None):
            id = uuid.uuid1()

        # Create a new hashtag
        user_hashtag = UserHashtag(
            id=id, hashtag_id=hashtag_id, user_id=user_id, userType=user.userType)

        # Add match to session.
        db.session.add(user_hashtag)

        # Commit session.
        db.session.commit()

        message.set_data({"id": user_hashtag.id})
        return message.SUCCESS

    def delete(self, user_id):
        # Unfollow a hashtag
        _ = get_user(user_id)

        try:
            json_data = request.get_json()
            hashtag_id = json_data['hashtag_id']
        except Exception as why:
            # Log input strip or etc. errors.
            logging.info("Given Data is wrong. " + str(why))

            message.set_data(
                {"hashtag_id": "Given hashtag id is wrong format"})
            return message.INVALID_INPUT_422

        # Find hashtag
        user_hashtag = UserHashtag.query.filter_by(
            hashtag_id=hashtag_id, user_id=user_id).first()

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


class UserFeed(Resource):
    method_decorators = [login_required]

    def get(self, user_id):
        _ = get_user(user_id)

        model = RecommenderModel()

        # Get similar users id list
        similar_user_ids = model.get_similar_users(user_id, num_users=1)

        # Filter only mentor ids
        similar_user_ids = [similar_user_id for similar_user_id in similar_user_ids if User.query.filter_by(
            id=similar_user_id).first().userType == "mentor"]

        message.set_data(
            {"id_lst": similar_user_ids})

        return message.SUCCESS
