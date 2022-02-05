import os
import configparser

import psycopg2
from flask import Flask, render_template, redirect, url_for, flash, request, g, make_response, jsonify
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from pairmaker_user import User
from pairmaker_database import Database
from pairmaker_utils import UserSelector
from pairmaker_answer_stringify import NumberToString, IdentikitPathBuilder
from pairmaker_handler import _key_values_dict, _check_img_format, _request_form_getter, _check_link_format, \
    _request_identikit_parser, _get_base_data_str, _get_form_data_str, _get_kit_data_str, amount

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
        checked = len(dbase.select_all_data_from_table_by_id(current_user.get_id(), 'form'))
        if checked > 0:
            return redirect(url_for('person_page', user_id=current_user.get_id()))
        else:
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
        checked = len(dbase.select_all_data_from_table_by_id(current_user.get_id(), 'form'))
        if checked > 0:
            return redirect(url_for('person_page', user_id=current_user.get_id()))
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
        dbase.update_identikit_set_all_null_by_user_id(current_user.get_id())
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
    link_vk = request.form.get('link_vk')
    link_inst = request.form.get('link_inst')
    link_num = request.form.get('link_num')
    if not any([link_vk, link_inst, link_num]):
        flash('Укажите хотя бы одну ссылку', category='alert-warning')
        return redirect(url_for('quest_block_5'))

    for link in [link_vk, link_inst, link_num]:
        if link and not _check_link_format(link):
            flash('Некорректная ссылка, повторите ввод', category='alert-warning')
            return redirect(url_for('quest_block_5'))

    if file and _check_img_format(file.filename):
        try:
            image = file.read()
        except FileNotFoundError:
            flash('Изображение не найдено', category='alert-warning')
            return redirect(url_for('quest_block_5'))
    else:
        flash('Некорректное изображение - требуется png формат', category='alert-warning')
        return redirect(url_for('quest_block_5'))

    current_id = current_user.get_id()
    if not (
            dbase.update_user_avatar(current_id, image) and
            dbase.update_user_links(current_id, [link_vk, link_inst, link_num])
    ):
        flash('Не удалось загрузить данные', category='alert-warning')
        return redirect(url_for('quest_block_5'))
    return redirect(url_for('person_page', user_id=current_user.get_id()))


@app.route('/userava/<int:user_id>')
@login_required
def userava(user_id: int):
    image: memoryview = dbase.select_user_avatar_by_id(user_id)
    image = image.tobytes()
    h = make_response(image)
    h.headers['Content-Type'] = 'image/png'
    return h


@app.route('/person-page/<user_id>')
def person_page(user_id: int):
    if not dbase.check_user_exist(user_id):
        flash('Данного пользователя не существует', category='alert-warning')
        return redirect(url_for('person_page', user_id=current_user.get_id()))

    current_id = current_user.get_id()
    base_user_data = dbase.select_all_data_from_table_by_id(user_id, 'users')
    identikit_data = dbase.select_all_data_from_table_by_id(user_id, 'identikit')
    form_data = dbase.select_all_data_from_table_by_id(user_id, 'form')
    image_paths = IdentikitPathBuilder.construct_image_paths(
        _get_kit_data_str(identikit_data),
        bool(base_user_data[4])
    )
    data = {
        'paths': image_paths,
        'present': _get_base_data_str(base_user_data),
        'form': _get_form_data_str(form_data, base_user_data)
    }
    if current_user.get_id() == user_id:
        own_profile = open_profile = True
    else:
        own_profile = open_profile = False

    return render_template('person-page.html',
                           title='Страница пользователя',
                           own=own_profile,
                           open=open_profile,
                           data=data,
                           id=int(user_id))


@app.route('/person-page-send', methods=['POST'])
def person_page_send():
    user_id = int(request.json.get('userId'))
    if dbase.insert_users_relations(current_user.get_id(), user_id):
        return jsonify({'sent': True})
    return jsonify({'sent': False})


@app.route('/view-page')
def view_page():
    person_ids, person_stages = [], []
    offset, limit, cap, req_stage = 0, 50, 50, 1
    current_id = current_user.get_id()
    selector = UserSelector(dbase.select_all_data_from_table_by_id(current_user.get_id(), 'form'))
    while True:
        persons_dump = dbase.select_persons_form_data(current_id, limit, offset)
        for person in persons_dump:
            stage = selector.juxtaposition(person)
            if stage >= req_stage:
                person_ids.append(person[0])
                person_stages.append(stage)

        if len(person_ids) >= 50 or len(persons_dump) < limit:
            break
        offset += limit

    persons = []
    for i, person_id in enumerate(person_ids):
        person_data = dbase.select_person_minimal_data(person_id)
        persons.append({
            'stage': person_stages[i],
            'id': person_data[0],
            'name': person_data[8],
            'paths': IdentikitPathBuilder.construct_image_paths(
                _get_kit_data_str(person_data[:8]),
                bool(person_data[9])
            )
        })
    persons.sort(key=lambda x: x['stage'], reverse=True)
    return render_template('view-page.html',
                           title='Ищу пару',
                           persons=persons,
                           selfid=current_id)


@app.route('/enter-requests')
def enter_requests():
    result = []
    data = dbase.select_user_enter_requests(current_user.get_id())
    print(data)
    for row in data:
        result.append({
            'id': row[0],
            'name': row[1]
        })
    return render_template('enter-requests.html',
                           title='Входящие запросы',
                           selfid=current_user.get_id(),
                           data=result)


@app.route('/enter-page-accept-requests', methods=['POST'])
def enter_request_accept_requests():
    user_id = int(request.json.get('toUser').split('_')[1])
    if dbase.update_users_relations(current_user.get_id(), user_id):
        return jsonify({'accepted': True})
    return jsonify({'accepted': False})


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
