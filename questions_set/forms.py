from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField
from wtforms import validators

__all__ = ('QuestionSetForm',)


class QuestionSetForm(FlaskForm):
    text = StringField('Назва тестового набору')
    submit = SubmitField('Додати тестовий набір')