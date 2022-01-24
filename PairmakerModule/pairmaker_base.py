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
from pairmaker_forms import Registerform, Loginform

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


@app.route('/')
def index():
    register_form = Registerform()
    login_form = Loginform()

    if current_user.is_authenticated:
        return redirect(url_for('quest'))

    return render_template('index.html',
                           title='Начало',
                           rform=register_form,
                           lform=login_form)


@app.route('/login', methods=['POST'])
def login():
    login_form = Loginform()
    if login_form.validate_on_submit():
        login = login_form.login_login.data
        password = login_form.login_pass.data
        userdata = User.userify(dbase.get_user_by_login(login))
        if userdata and check_password_hash(userdata['phash'], password):
            userlogin = User().create(userdata)
            login_user(userlogin)
            return redirect(url_for('quest'))
        else:
            flash('Логин или пароль неверны', category='alert-warning')
    else:
        flash('Авторизация не удалась', category='alert-warning')

    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    register_form = Registerform()
    if register_form.validate_on_submit():
        fname = register_form.register_fname.data
        lname = register_form.register_lname.data
        login = register_form.register_login.data
        password = register_form.register_pass.data

        if dbase.register_new_user(fname, lname, login,
                                   generate_password_hash(password)):
            userdata = User.userify(dbase.get_user_by_login(login))
            userlogin = User().create(userdata)
            login_user(userlogin)
            return redirect(url_for('quest'))
        else:
            flash('Данный логин уже зарегистрирован', category='alert-warning')
    else:
        flash('Регистрация не удалась', category='alert-warning')
    return redirect(url_for('index'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы успешно вышли из аккаунта', category='alert-success')
    return redirect(url_for('index'))


@app.route('/quest')
def quest():
    # Check marked questions
    return redirect(url_for('quest_block_1'))


@app.route('/quest-block-1', methods=['GET', 'POST'])
def quest_block_1():
    if request.method == 'POST':
        answers = dict(request.form)
        dbase.paste_answers_from_dict(answers, current_user.get_id())
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


@app.route('/quest-block-3', methods=['GET', 'POST'])
def quest_block_3():
    if request.method == 'POST':
        # DB answers paste
        return redirect(url_for(''))
    return render_template('quest-block-3.html',
                           title='Блок вопросов')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
