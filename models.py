import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

import config

DATABASE = SqliteDatabase(config.DB_NAME)


class User(UserMixin, Model):
    username = CharField(unique=True)
    email = CharField(unique=True)
    password = CharField(max_length=100)
    joined_at = DateTimeField(default=datetime.datetime.now)

    class Meta:
        database = DATABASE
        order_by = ('-joined_at')

    @classmethod
    def create_user(cls, username, email, password):
        try:
            with DATABASE.transaction():
                cls.create(
                    username=username,
                    email=email,
                    password=generate_password_hash(password),
                )
        except IntegrityError:
            raise ValueError("User already exists!")


class Entry(Model):
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='entries')
    slug = CharField(unique=True, max_length=50)
    title = CharField(max_length=100)
    date = DateTimeField()
    time_spent = IntegerField()
    subjects = TextField()
    resources = TextField()

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)


class Tag(Model):
    tag = CharField(unique=True, max_length=100)

    class Meta:
        database = DATABASE


class TagEntry(Model):
    tag = ForeignKeyField(Tag, backref='tags')
    entry = ForeignKeyField(Entry, backref='entries')


    class Meta:
        database = DATABASE
        indexes = (
            (('entry', 'tag'), True),
        )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, TagEntry], safe=True)
    DATABASE.close()
