from flask import url_for
from flask_login import UserMixin


class User(UserMixin):
    def create(self, user):
        self.__user = user
        return self

    def load_from_db(self, user_id, db):
        self.__user = db.select_user_by_id(user_id)
        return self

    def get_id(self):
        self.__user = self.userify(self.__user)
        return str(self.__user['id'])

    def get_name(self):
        self.__user = self.userify(self.__user)
        return self.__user['firstname']

    @classmethod
    def userify(cls, data):
        if type(data) is dict:
            return data
        elif type(data) in [tuple, list]:
            return {
                'id': data[0],
                'firstname': data[1],
                'login': data[2],
                'passhash': data[3],
                'avatar': data[4]
            }
        return None
