import implicit  # Library for recommendation
import numpy as np
from scipy.sparse import csr_matrix
from app.models import User, Hashtag, UserHashtag


class RecommenderModel():
    def __init__(self):
        self.model = implicit.als.AlternatingLeastSquares()
        self.update()

    def update(self):
        self.user_hashtags = UserHashtag.query.all()
        users = User.query.all()
        hashtags = Hashtag.query.all()
        self.user_ids = [user.id for user in users]
        self.hashtag_ids = [hashtag.id for hashtag in hashtags]

        # This will be our data for sparse array
        self.data = np.array([1 for user_hashtag in self.user_hashtags])

        # Row and col stores the row/col index of each data
        row_lst = []
        col_lst = []

        for user_hashtag in self.user_hashtags:
            col_lst.append(self.user_ids.index(user_hashtag.user_id))
            row_lst.append(self.hashtag_ids.index(user_hashtag.hashtag_id))

        # Change to numpy array
        row = np.array(row_lst)
        col = np.array(col_lst)

        self.hashtag_user_data = csr_matrix(
            (self.data, (row, col)), shape=(len(self.hashtag_ids), len(self.user_ids)))

        # train the model on a sparse matrix of hashtag/user/confidence weights
        self.model.fit(self.hashtag_user_data)

    def get_similar_users(self, user_id, num_users):
        row_id = self.user_ids.index(user_id)
        related = self.model.similar_users(row_id, num_users)
        similar_users = [self.user_ids[index] for (index, _) in related]
        return similar_users

    def recommend_hashtags(self, user_id, num_items):
        # recommend hashtags for a user
        user_items = self.hashtag_user_data.T.tocsr()
        row_id = self.user_ids.index(user_id)
        recommendations = self.model.recommend(row_id, user_items, num_items)
        return recommendations
