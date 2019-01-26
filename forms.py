from flask_wtf import FlaskForm as Form
from wtforms import (StringField, PasswordField, TextAreaField, DateField,
                     IntegerField)
from wtforms.validators import (DataRequired, Regexp, Email, Length)

from models import Tag


def tag_exists(form, field):
    if Tag.select().where(Tag.tag == field.data).exists():
        pass


class LoginForm(Form):
    email = StringField(
        'Email',
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        'Password',
        validators=[DataRequired()]
    )


class EntryForm(Form):
    title = StringField(
        'Title*',
        validators=[DataRequired(), Length(min=3, max=100)])
    date = DateField(
        'Date (DD/MM/YYYY)*',
        format='%d/%m/%Y',
        validators=[DataRequired(
            message="Please enter a valid date.")])
    time_spent = IntegerField(
        'Time spent (Minutes)*',
        validators=[DataRequired(message="Please enter a valid number.")])
    subjects = TextAreaField(
        'What You Learned*',
        validators=[DataRequired()])
    resources = TextAreaField(
        'Resources to Remember',
        validators=[])
    tags = StringField(
        'Tags (Seperate tags with comma)')
    validators = [
        Regexp(
            r'^[a-zA-Z0-9,]+$',
            message=("tags should be letters, "
                     "and should be seperated by comma.")
        )]


class TagForm(Form):
    tag = StringField(
        'Tag',
        validators=[
            DataRequired(),
            Length(min=3, max=100),
            tag_exists
        ])
