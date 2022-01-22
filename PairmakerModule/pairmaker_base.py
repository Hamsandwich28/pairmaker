import os
from flask import Flask, render_template, redirect, url_for, \
    flash, jsonify, request
from flask_login import LoginManager, login_user, login_required, \
    logout_user, current_user

from pairmaker_user import User
from pairmaker_forms import Registerform, Loginform


# config
app = Flask(__name__)
app.config['SECRET_KEY'] = '533899465101462ae6122972'
app.config['MAX_CONTENT_LENGTH'] = 1024 * 1024

# loginmanager
# login_manage = LoginManager(app)
# login_manage.login_view = 'index'


@app.route('/')
def index():
    register_form = Registerform()
    login_form = Loginform()

    # if current_user.is_authenticated:
    #     return redirect(url_for('quest'))

    return render_template('index.html',
                           title='Начало',
                           rform=register_form,
                           lform=login_form)


@app.route('/login', methods=['POST'])
def login():
    login_form = Loginform()
    if login_form.validate_on_submit():
        # Get password hash and register new user
        # Create current user
        return redirect(url_for('quest'))
    else:
        flash('Авторизация не удалась', category='alert-warning')
        return redirect(url_for('index'))


@app.route('/register', methods=['POST'])
def register():
    register_form = Registerform()
    if register_form.validate_on_submit():
        # Get password hash and check at db
        # Create current user
        return redirect(url_for('quest'))
    else:
        flash('Регистрация не удалась', category='alert-warning')
        return redirect(url_for('index'))


@app.route('/quest')
def quest():
    return render_template('quest.html',
                           title='Вопросы')


@app.route('/quest_answer', methods=['POST'])
def quest_answer():
    # Set question answer
    return jsonify({'set': True})


if __name__ == '__main__':
    app.run(host='localhost', port=5000)
