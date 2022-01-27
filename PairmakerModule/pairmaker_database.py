import psycopg2
from typing import Optional


class Database:
    db_instance = None

    def __new__(cls, *args, **kwargs):
        if not cls.db_instance:
            cls.db_instance = super().__new__(cls)
        return cls.db_instance

    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()

    def _insert_empty_to_form_table(self, user_id: int) -> None:
        """Установка записи ответов - изначально с пустыми полями"""
        sql = f"INSERT INTO form(user_id) VALUES(%s);"
        self.__cur.execute(sql, user_id)

    def _insert_empty_to_identikit_table(self, user_id: int) -> None:
        """Установка записи ответов - изначально с пустыми полями"""
        sql = f"INSERT INTO identikit(user_id) VALUES(%s);"
        self.__cur.execute(sql, user_id)

    def insert_new_user(self, firstname: str, login: str, passhash: str) -> bool:
        """Запрос на вставку новой записи пользователя"""
        try:
            sql = """
            INSERT INTO users (firstname, login, passhash)
            VALUES(%s, %s, %s)
            RETURNING id;"""
            self.__cur.execute(sql, (firstname, login, passhash))
            new_user_id = self.__cur.fetchone()
            self._insert_empty_to_form_table(new_user_id)
            self._insert_empty_to_identikit_table(new_user_id)
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print('Ошибка добавления пользователя -> ', e)
        return False

    def select_user_by_id(self, user_id: int) -> Optional[tuple]:
        """Выборка записи пользователя по id"""
        try:
            sql = f"SELECT * FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def select_user_by_login(self, user_login: str) -> Optional[tuple]:
        """Выборка записи пользователя по логину"""
        try:
            sql = f"SELECT * FROM users WHERE login = '{user_login}';"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def update_table_from_dict_by_user_id(self,
                                          user_id: int,
                                          table: str,
                                          answers: dict) -> bool:
        """Обновление записи указанной таблицы по id пользователя """
        set_str = ', '.join([f'{k} = {int(v) if v else "NULL"}'
                             for k, v in answers.items()])
        try:
            sql = f"""UPDATE {table} SET {set_str} WHERE user_id = {user_id};"""
            self.__cur.execute(sql)
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print(f'Ошибка установки записи таблицы {table} -> ', e)
        return False

    def select_answers_form_blocks(self, user_id: int) -> Optional[tuple]:
        try:
            sql = f"""
            SELECT 
            ismale, age, growth,
            sportattitude, movieattitude1, movieattitude2,
            litattitude1, litattitude2, hobbi1, hobbi2
            FROM form
            WHERE user_id = {user_id};"""
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            return res

        except psycopg2.Error as e:
            print('Ошибка чтения записей ответов -> ', e)
        return None

    def update_user_avatar_and_link(self, user_id: int, image, link) -> bool:
        if not image:
            return False
        binary = psycopg2.Binary(image)
        try:
            sql = """
            UPDATE users SET 
            avatar = %s,
            social = %s
            WHERE id = %s;
            """
            self.__cur.execute(sql, (binary, link, user_id))
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print('Ошибка чтения записей ответов -> ', e)
        return False
