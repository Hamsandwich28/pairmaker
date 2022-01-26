import os
import configparser
import psycopg2
from flask import Flask, render_template, redirect, url_for, \
    flash, jsonify, request, g
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from pairmaker_user import User
from pairmaker_database import Database

# config
app = Flask(__name__)
app.config['SECRET_KEY'] = '533899465101462ae6122972'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

# database config
conf_name = 'settings.ini'
config = configparser.ConfigParser()
config.read(os.path.join(app.root_path, conf_name))
dbase = None

# loginmanager
login_manage = LoginManager(app)
login_manage.login_view = 'index'
login_manage.login_message = 'Пожалуйста, авторизуйтесь на сайте'
login_manage.login_message_category = 'alert-warning'


@login_manage.user_loader
def load_user(user_id):
    return User().load_from_db(user_id, dbase)


# database connectors
def connect_db():
    global config
    params = dict(config['Database'])
    connect = psycopg2.connect(**params)
    return connect


def get_db():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db


@app.before_request
def before_request():
    global dbase
    db = get_db()
    dbase = Database(db)


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта', category='alert-success')
    return redirect(url_for('index'))


@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('quest'))

    return render_template('index.html',
                           title='Начало')


@app.route('/login', methods=['POST'])
def login():
    login = request.form.get('login')
    password = request.form.get('password')
    userdata = User.userify(dbase.select_user_by_login(login))
    if userdata and check_password_hash(userdata['passhash'], password):
        userlogin = User().create(userdata)
        login_user(userlogin)
        return redirect(url_for('quest'))
    else:
        flash('Логин или пароль неверны', category='alert-warning')

    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get('firstname')
    login = request.form.get('login')
    password = request.form.get('password')
    if len(fname) < 2 or len(login) < 6 or len(password) < 6:
        flash('Некорректные данные полей', category='alert-warning')
        return redirect(url_for('index'))

    if dbase.insert_new_user(firstname, login, generate_password_hash(password)):
        userdata = User.userify(dbase.select_user_by_login(login))
        userlogin = User().create(userdata)
        login_user(userlogin)
        return redirect(url_for('quest'))
    else:
        flash('Данный логин уже зарегистрирован', category='alert-warning')
        return redirect(url_for('index'))


@app.route('/quest')
def quest():
    # Check marked questions
    return redirect(url_for('quest_block_1'))


@app.route('/quest-block-1', methods=['GET', 'POST'])
def quest_block_1():
    if request.method == 'POST':
        answers_paste = {
            'ismale': request.form.get('ismale'),
            'age': request.form.get('age'),
            'growth': request.form.get('growth')
        }
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'form', answers_paste
        )
        return redirect(url_for('quest_block_2'))
    return render_template('quest-block-1.html',
                           title='Блок вопросов')


@app.route('/quest-block-2', methods=['GET', 'POST'])
def quest_block_2():
    if request.method == 'POST':
        # DB answers paste
        return redirect(url_for('quest_block_3'))
    return render_template('quest-block-2.html',
                           title='Блок вопросов')


def _key_values_dict(obj, basename):
    result = {
        basename + str(1): None,
        basename + str(2): None
    }
    posted = 0
    for row in obj:
        if row:
            result[basename + str(posted + 1)] = row
            posted += 1
        if posted == 2:
            break
    return result


@app.route('/quest-block-3', methods=['GET', 'POST'])
def quest_block_3():
    if request.method == 'POST':
        movie = [
            request.form.get('movieattitude0') or None,
            request.form.get('movieattitude1') or None,
            request.form.get('movieattitude2') or None,
            request.form.get('movieattitude3') or None
        ]
        lit = [
            request.form.get('litattitude0') or None,
            request.form.get('litattitude1') or None,
            request.form.get('litattitude2') or None,
            request.form.get('litattitude3') or None,
        ]
        answers_paste = {
            'sportattitude': request.form.get('sportattitude'),
        }
        answers_paste.update(_key_values_dict(movie, 'movieattitude'))
        answers_paste.update(_key_values_dict(lit, 'litattitude'))
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'form', answers_paste
        )
        # return redirect(url_for(''))
    return render_template('quest-block-3.html',
                           title='Блок вопросов')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
