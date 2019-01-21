from datetime import datetime

from flask_wtf import FlaskForm as Form
from wtforms import (StringField, PasswordField, TextAreaField, DateField,
                     IntegerField, SelectMultipleField)
from wtforms.validators import (DataRequired, Regexp, ValidationError,
                                Email, Length, EqualTo)

from models import Tag


# def get_tags():
#     tags = [(Tag, Tag) for Tag in Tag.select()]
#     return tags


def tag_exists(form, field):
    if Tag.select().where(Tag.tag == field.data).exists():
        raise ValidationError('Tag already exists.')


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
        'Title',
        validators=[DataRequired(), Length(min=3, max=100)])
    slug = StringField(
        'URL Slug',
        validators=[
            DataRequired(),
            Length(min=3, max=50),
            Regexp(
                r'^[a-zA-Z0-9_-]+$',
                message=("Url slug should be letters, "
                         "numbers, dash and underscores only.")
            )]
    )
    date = DateField(
        'Date',
        validators=[DataRequired])
    time_spent = IntegerField(
        'Time spent',
        validators=[DataRequired])
    subjects = TextAreaField(
        'What You Learned',
        validators=[DataRequired])
    resources = TextAreaField(
        'Resources to Remember',
        validators=[])
    # tags = SelectMultipleField(choices=get_tags())


class TagForm(Form):
    tag = StringField(
        'Tag',
        validators=[
            DataRequired(),
            Length(min=3, max=100),
            tag_exists
        ])
