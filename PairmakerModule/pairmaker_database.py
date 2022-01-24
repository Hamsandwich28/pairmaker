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
                      VALUES(%s, %s, %s, %s)
                      RETURNING id;"""
            self.__cur.execute(sql, (fname, lname, login, phash))
            new_user_id = self.__cur.fetchone()

            sql = f"""INSERT INTO question_table (userId)
                      VALUES(%s);"""
            self.__cur.execute(sql, new_user_id)
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
            res = self.__cur.fetchone()
            if res:
                return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

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

    def paste_answers_from_dict(self, answers: dict, user_id):
        set_str = ', '.join([f'{k} = {int(v)}' for k, v in answers.items()])
        try:
            sql = f"""UPDATE question_table
                      SET {set_str}
                      WHERE userId = {user_id};"""
            self.__cur.execute(sql)
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print('Ошибка установки ответов пользователя -> ', e)

