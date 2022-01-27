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
from pairmaker_handler import _key_values_dict, _check_img_format, \
    _check_link_format

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
    if len(firstname) < 2 or len(login) < 6 or len(password) < 6:
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
    check_form = dbase.select_answers_form_blocks(current_user.get_id())
    # check_block2 = dbase.select_user_idenikit(current_user.get_id())
    # check_info = dbase.select_user_info(current_user.get_id())
    block1, block3 = check_form[:3], check_form[3:]
    if None in block1:
        return redirect(url_for('quest_block_1'))
    # elif None in check_block2:
    #     return redirect(url_for('quest_block_2'))
    elif None in block3:
        return redirect(url_for('quest_block_3'))
    # elif None in check_info:
    #     return redirect(url_for('personal_info'))
    return redirect(url_for('main_page'))


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


@app.route('/quest-block-3', methods=['GET', 'POST'])
def quest_block_3():
    if request.method == 'POST':
        movie = [
            request.form.get(k)
            for k in request.form.keys()
            if "movieattitude" in k
        ]
        lit = [
            request.form.get(k)
            for k in request.form.keys()
            if "litattitude" in k
        ]
        if not any(movie) or not any(lit):
            flash('Ответьте на каждый вопрос', category='alert-warning')
            return render_template('quest-block-3.html',
                                   title='Блок вопросов')
        answers_paste = {
            'sportattitude': request.form.get('sportattitude'),
        }
        answers_paste.update(_key_values_dict(movie, 'movieattitude', 2))
        answers_paste.update(_key_values_dict(lit, 'litattitude', 2))
        dbase.update_table_from_dict_by_user_id(
            current_user.get_id(), 'form', answers_paste
        )
        return redirect(url_for('personal_info'))
    return render_template('quest-block-3.html',
                           title='Блок вопросов')


@app.route('/personal-info')
def personal_info():
    return render_template('personal-info.html')


@app.route('/personal-info', methods=['POST'])
def personal_info_upload():
    file = request.files.get('file')
    link = request.form.get('link')
    if file and _check_img_format(file.filename) and _check_link_format(link):
        try:
            image = file.read()
            if not dbase.update_user_avatar_and_link(current_user.get_id(), image, link):
                flash('Изображение не удалось загрузить', category='alert-warning')
                return redirect(url_for('personal_info'))
        except FileNotFoundError:
            flash('Изображение не найдено', category='alert-warning')
            return redirect(url_for('personal_info'))
    else:
        flash('Некорректные данные (фото в png формате должно быть)', category='alert-warning')
        return redirect(url_for('personal_info'))

    return redirect(url_for('main_page'))


@app.route('/main-page')
def main_page():
    return render_template('main-page.html')


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
