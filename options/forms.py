from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField
from wtforms import validators

__all__ = ('OptionForm',)


class OptionForm(FlaskForm):
    question_pk = IntegerField()
    text = StringField('Текст варіанту відповіді')
    submit = SubmitField('Додати варіант відповіді')