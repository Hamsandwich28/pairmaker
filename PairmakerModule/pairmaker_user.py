from flask import url_for
from flask_login import UserMixin


class User(UserMixin):
    def create(self, user):
        self.__user = user
        return self

    @classmethod
    def userify(cls, data):
        return {
            'fname': '',        # firstname
            'lname': '',        # lastname
            'login': '',        # login
            'phash': '',        # passhash
            'picture': '',      # real picture
            'photorobot': ''    # selected photo
        }
