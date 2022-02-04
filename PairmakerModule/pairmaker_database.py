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
        sql = f"INSERT INTO form(id) VALUES(%s);"
        self.__cur.execute(sql, user_id)

    def _insert_empty_to_identikit_table(self, user_id: int) -> None:
        """Установка записи ответов - изначально с пустыми полями"""
        sql = f"INSERT INTO identikit(id) VALUES(%s);"
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

    def select_user_is_male(self, user_id: int) -> Optional[bool]:
        """Получение мужчина ли пользователь по id"""
        try:
            sql = f"SELECT ismale FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            return bool(res[0])

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def select_user_base_data(self, user_id: int) -> Optional[tuple]:
        """Получение данных имя, пола, возраста, роста пользователя по id"""
        try:
            sql = f"SELECT firstname, ismale, age, growth FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def select_all_data_from_table_by_id(self,
                                         user_id: int,
                                         table: str) -> Optional[tuple]:
        """Получение всех данных из таблицы по id"""
        try:
            sql = f"SELECT * FROM {table} WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def select_user_avatar_by_id(self, user_id: int) -> Optional[memoryview]:
        try:
            sql = f"SELECT avatar FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res[0]

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    def select_user_social_by_id(self, user_id: int) -> Optional[tuple]:
        try:
            sql = f"SELECT social FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return res[0]

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return None

    # relations

    def select_user_relations(self, ourid: int) -> list:
        try:
            sql = f"SELECT theirid, status FROM relations WHERE ourid = {ourid};"
            self.__cur.execute(sql)
            res = list(self.__cur.fetchall())
            return res
        except psycopg2.Error as e:
            print('Ошибка чтения записей отношений -> ', e)
        return []

    def select_user_enter_application(self, theirid: int) -> list:
        try:
            sql = f"SELECT theirid, status FROM relations WHERE theirid = {theirid};"
            self.__cur.execute(sql)
            res = list(self.__cur.fetchall())
            return res
        except psycopg2.Error as e:
            print('Ошибка чтения записей отношений -> ', e)
        return []

    def load_persons_form_data(self, except_id: int, limit: int, offset: int) -> list:
        try:
            sql = f"SELECT * FROM form WHERE id <> {except_id} LIMIT {limit} OFFSET {offset};"
            self.__cur.execute(sql)
            res = self.__cur.fetchall()
            return res

        except psycopg2.Error as e:
            print('Ошибка чтения записей отношений -> ', e)
        return []

    def check_users_relation(self, ourid: int, theirid: int) -> Optional[int]:
        try:
            sql = f"SELECT theirid, status FROM relations WHERE ourid = {ourid} AND theirid = {theirid};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            return res
        except psycopg2.Error as e:
            print('Ошибка чтения записей отношений -> ', e)
        return None

    def check_user_exist_by_id(self, user_id: int) -> bool:
        try:
            sql = f"SELECT firstname FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if len(res) > 0:
                return True

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return False

    def check_user_has_pair(self, user_id: int) -> bool:
        try:
            sql = f"SELECT pair FROM users WHERE id = {user_id};"
            self.__cur.execute(sql)
            res = self.__cur.fetchone()
            if res:
                return True

        except psycopg2.Error as e:
            print('Ошибка чтения пользователя -> ', e)
        return False

    def update_table_from_dict_by_user_id(self,
                                          user_id: int,
                                          table: str,
                                          answers: dict) -> bool:
        """Обновление записи указанной таблицы по id пользователя """
        set_str = ', '.join([f'{k} = {int(v) if v else "NULL"}'
                             for k, v in answers.items()])
        try:
            sql = f"""UPDATE {table} SET {set_str} WHERE id = {user_id};"""
            self.__cur.execute(sql)
            self.__db.commit()
            return True

        except psycopg2.Error as e:
            self.__db.rollback()
            print(f'Ошибка установки записи таблицы {table} -> ', e)
        return False

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
            print('Ошибка обновления записей ответов -> ', e)
        return False

    def update_identikit_set_all_null_by_user_id(self, user_id: int) -> bool:
        try:
            sql = f"""
            UPDATE identikit SET
            brows = NULL, eyes = NULL, hair = NULL,
            lips = NULL, nose = NULL, beard = NULL, addition = NULL
            WHERE id = {user_id};"""
            self.__cur.execute(sql)
            return True

        except psycopg2.Error as e:
            print('Ошибка обновления записей ответов -> ', e)
        return False
