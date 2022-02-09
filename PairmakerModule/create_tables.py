import os
import psycopg2
import configparser

SQL_FILE_NAME = "self_create_db.sql"


def _connect():
    conf_name = 'settings.ini'
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(os.path.realpath(__file__)), conf_name))
    params = dict(config['Database'])
    return psycopg2.connect(**params)


if __name__ == "__main__":
    connection = _connect()
    cursor = connection.cursor()
    with open(os.path.join(os.path.dirname(os.path.realpath(__file__)), SQL_FILE_NAME), 'r') as file:
        commands = file.read()
        sqlmany = [command + ';' for command in commands.split(';') if len(command) > 10]
        for sql in sqlmany:
            try:
                cursor.execute(sql)
            except psycopg2.Error as e:
                pass
    connection.commit()
    cursor.close()
    connection.close()
