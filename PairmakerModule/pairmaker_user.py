from flask import url_for
from flask_login import UserMixin


class User(UserMixin):
    def create(self, user):
        self.__user = user
        return self

    def load_from_db(self, user_id, db):
        self.__user = db.get_user_by_id(user_id)
        return self

    def get_id(self):
        return str(self.__user['id'])

    @classmethod
    def userify(cls, data):
        return {
            'id': data[0],               # id
            'fname': data[1],            # firstname
            'lname': data[2],            # lastname
            'login': data[3],            # login
            'phash': data[4],            # passhash
            'avatar': data[5],           # real picture
            'indentikit': data[6],       # selected photo
            'user_bound': data[7],       # users activity
            'answer_list': data[8]       # checked questions
        } if data else None
