import psycopg2


class Database:
    db_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.db_instance:
            cls.db_instance = super().__new__(cls)
        return cls.db_instance

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def register_new_user(self, fname, lname, login, phash):
        try:
            sql = f"""INSERT INTO users (firstname, lastname, login, phash)
                      VALUES(%s, %s, %s, %s);"""
            self.__cur.execute(sql, (fname, lname, login, phash))
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print('Ошибка добавления пользователя -> ', e)
        return False

    def get_user_by_login(self, login):
        try:
            sql = f"""SELECT *
                      FROM users
                      WHERE login = '{login}';"""
            self.__cur.execute(sql)
            res = self.__cur.fetchone() or None
            return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)

    def get_user_by_id(self, user_id):
        try:
            sql = f"""SELECT *
                      FROM users
                      WHERE id = {user_id};"""
            self.__cur.execute(sql)
            res = self.__cur.fetchone() or None
            return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
