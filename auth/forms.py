from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms import validators

__all__ = ('RegistrationForm', 'LoginForm')

class RegistrationForm(FlaskForm):
    username = StringField('Логін', validators=[validators.DataRequired(message='Поле обов`язкове')])
    password = PasswordField('Пароль',
                             validators=[
                                 validators.DataRequired(message='Поле обов`язкове'),
                                 validators.EqualTo('confirm', message='Паролі повинні співпадати')])
    confirm = PasswordField('Повторіть пароль', validators=[validators.DataRequired(message='Поле обов`язкове')])
    full_name = StringField('Як до вас звертатися?', validators=[validators.DataRequired(message='Поле обов`язкове')])
    submit = SubmitField('Зареєструватися')


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[validators.DataRequired(message='Поле обов`язкове')])
    password = PasswordField('Password', validators=[validators.DataRequired(message='Поле обов`язкове')])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')