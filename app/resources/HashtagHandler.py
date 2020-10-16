import logging
import uuid
from flask_login import login_required, fresh_login_required
from flask import g, request, jsonify
from flask_restful import Resource
from app.models import User, Hashtag, UserHashtag
from app.utils.recommender import RecommenderModel
from app.resources.UserHandler import login_manager, type_required, get_user
from app.messages import Message
from app.database import db


message = Message()


def hashtag_loader(id):
    hashtag = Hashtag.query.filter_by(id=id).first()
    return hashtag


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
        similar_user_ids = model.get_similar_users(user_id, num_users=10)

        # Filter only mentor ids
        similar_user_ids = [similar_user_id for similar_user_id in similar_user_ids if User.query.filter_by(
            id=similar_user_id).first().userType == "mentor"]

        message.set_data(
            {"id_lst": similar_user_ids})

        return message.SUCCESS
