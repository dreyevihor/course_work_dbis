from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, HiddenField, IntegerField
from wtforms import validators

__all__ = ('QuestionForm',)


class QuestionForm(FlaskForm):
    set_pk = IntegerField()
    text = StringField('Текст запитання')
    submit = SubmitField('Додати запитання')