from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class Registerform(FlaskForm):
    register_fname = StringField('Имя',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите имя',
                                            'class': 'form-control'})
    register_lname = StringField('Фамилия',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите фамилию',
                                            'class': 'form-control'})
    register_login = StringField('Логин',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите логин',
                                            'class': 'form-control'})
    register_pass = PasswordField('Пароль',
                                  validators=[DataRequired(), Length(min=4, max=20)],
                                  render_kw={'placeholder': 'Введите пароль',
                                             'class': 'form-control'})
    register_submit = SubmitField('Начать',
                                  render_kw={'class': 'btn btn-primary',
                                             'id': 'register-submit'})


class Loginform(FlaskForm):
    login_login = StringField('Логин',
                              validators=[DataRequired()],
                              render_kw={'placeholder': 'Введите логин',
                                         'class': 'form-control'})
    login_pass = PasswordField('Пароль',
                               validators=[DataRequired(), Length(min=4, max=20)],
                               render_kw={'placeholder': 'Введите пароль',
                                          'class': 'form-control'})
    login_submit = SubmitField('Начать',
                               render_kw={'class': 'btn btn-primary',
                                          'id': 'login-submit'})
