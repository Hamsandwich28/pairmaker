from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length


class Registerform(FlaskForm):
    register_fname = StringField('Имя',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите имя'})
    register_lname = StringField('Фамилия',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите фамилию'})
    register_login = StringField('Логин',
                                 validators=[DataRequired()],
                                 render_kw={'placeholder': 'Введите логин'})
    register_pass = PasswordField('Пароль',
                                  validators=[DataRequired(), Length(min=4, max=20)],
                                  render_kw={'placeholder': 'Введите пароль'})
    register_submit = SubmitField('Начать',
                                  render_kw={})


class Loginform(FlaskForm):
    login_login = StringField('Логин',
                              validators=[DataRequired()],
                              render_kw={'placeholder': 'Введите логин'})
    login_pass = PasswordField('Пароль',
                               validators=[DataRequired(), Length(min=4, max=20)],
                               render_kw={'placeholder': 'Введите пароль'})
    login_submit = SubmitField('Начать',
                               render_kw={})
