import os
import configparser

import psycopg2
from flask import Flask, render_template, redirect, url_for, flash, request, g, make_response
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from pairmaker_user import User
from pairmaker_database import Database
from pairmaker_handler import _key_values_dict, _check_img_format, _request_form_getter, _check_link_format, \
    _request_identikit_parser, _get_user_full_data, amount
from pairmaker_dict import NumberToString, IdentikitPathBuilder

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
        return redirect(url_for('quest_block_1'))

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
        return redirect(url_for('quest_block_1'))
    else:
        flash('Логин или пароль неверны', category='alert-warning')

    return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    firstname = request.form.get('firstname')
    login = request.form.get('login')
    password = request.form.get('password')
    if len(firstname) < 2 or len(login) < 6 or len(password) < 6:
        flash('Некорректные данные полей', category='alert-warning')
        return redirect(url_for('index'))

    if dbase.insert_new_user(firstname, login, generate_password_hash(password)):
        userdata = User.userify(dbase.select_user_by_login(login))
        userlogin = User().create(userdata)
        login_user(userlogin)
        return redirect(url_for('quest_block_1'))
    else:
        flash('Данный логин уже зарегистрирован', category='alert-warning')
        return redirect(url_for('index'))


@app.route('/quest-block-1', methods=['GET', 'POST'])
def quest_block_1():
    if request.method == 'POST':
        answers_paste = {
            'ismale': request.form.get('ismale'),
            'age': request.form.get('age'),
            'growth': request.form.get('growth')
        }
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'users', answers_paste
        )
        return redirect(url_for('quest_block_2'))
    return render_template('quest-block-1.html',
                           title='Блок вопросов')


@app.route('/quest-block-2', methods=['GET', 'POST'])
def quest_block_2():
    if request.method == 'POST':
        kit = _request_identikit_parser(request)
        print(kit)
        dbase.update_table_from_dict_by_user_id(current_user.get_id(), 'identikit', kit)
        return redirect(url_for('quest_block_3'))
    ismale = dbase.select_user_is_male(current_user.get_id())
    if ismale is None:
        return redirect(url_for('quest_block_1'))

    return render_template('quest-block-2.html',
                           title='Блок вопросов',
                           ismale='m' if ismale else 'f',
                           amount=amount)


@app.route('/quest-block-3', methods=['GET', 'POST'])
def quest_block_3():
    if request.method == 'POST':
        hobby = _request_form_getter(request, 'hobby')
        if not any(hobby):
            flash('Ответьте на каждый вопрос', category='alert-warning')
            return render_template('quest-block-3.html',
                                   title='Блок вопросов')
        answers_paste = {'sportattitude': request.form.get('sportattitude')}
        answers_paste.update(_key_values_dict(hobby, 'hobby', 2))
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'form', answers_paste
        )
        return redirect(url_for('quest_block_4'))
    return render_template('quest-block-3.html',
                           title='Блок вопросов')


@app.route('/quest-block-4', methods=['GET', 'POST'])
def quest_block_4():
    if request.method == 'POST':
        movie = _request_form_getter(request, 'movieattitude')
        lit = _request_form_getter(request, 'litattitude')
        if not any(movie) or not any(lit):
            flash('Ответьте на каждый вопрос', category='alert-warning')
            return render_template('quest-block-4.html',
                                   title='Блок вопросов')
        answers_paste = {}
        answers_paste.update(_key_values_dict(movie, 'movieattitude', 2))
        answers_paste.update(_key_values_dict(lit, 'litattitude', 2))
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'form', answers_paste
        )
        return redirect(url_for('quest_block_5'))
    return render_template('quest-block-4.html',
                           title='Блок вопросов')


@app.route('/quest-block-5')
def quest_block_5():
    return render_template('quest-block-5.html',
                           title='Блок вопросов')


@app.route('/quest-block-5', methods=['POST'])
def quest_block_5_upload():
    file = request.files.get('file')
    link = request.form.get('link')
    if file and _check_img_format(file.filename) and _check_link_format(link):
        try:
            image = file.read()
            if not dbase.update_user_avatar_and_link(current_user.get_id(), image, link):
                flash('Изображение не удалось загрузить', category='alert-warning')
                return redirect(url_for('quest_block_5'))
        except FileNotFoundError:
            flash('Изображение не найдено', category='alert-warning')
            return redirect(url_for('quest_block_5'))
    else:
        flash('Некорректные данные, повторите ввод', category='alert-warning')
        return redirect(url_for('quest_block_5'))

    return redirect(url_for('person_page', user_id=current_user.get_id()))


@app.route('/userava')
def userava():
    img = current_user.get_avatar()
    if not img:
        return ''

    h = make_response(img)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/person-page/<user_id>')
def person_page(user_id: int):
    if not dbase.check_user_exist_by_id(user_id):
        flash('Данный пользователь не зарегистрирован', 'alert-warning')
        return redirect(url_for('person_page', user_id=current_user.get_id()))
    base_user_data = dbase.select_user_base_data(user_id)
    identikit_data = dbase.select_all_data_from_table_by_id(user_id, 'identikit')
    form_data = dbase.select_all_data_from_table_by_id(user_id, 'form')
    user_gender = bool(base_user_data[1])
    full_data = _get_user_full_data(base_user_data, identikit_data, form_data)
    image_paths = IdentikitPathBuilder.construct_image_paths(full_data['identikit'], user_gender)
    open_profile = current_user.get_id() == user_id or current_user.get_pair() == user_id
    return render_template('person-page.html',
                           title='Страница пользователя',
                           open=open_profile,
                           data=full_data,
                           paths=image_paths)


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
