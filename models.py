import datetime

from flask_bcrypt import generate_password_hash
from flask_login import UserMixin
from peewee import *

import config

DATABASE = SqliteDatabase(config.DB_NAME)


class User(UserMixin, Model):
    """
    User Model
    """
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
    """
    Entry model
    """
    timestamp = DateTimeField(default=datetime.datetime.now)
    user = ForeignKeyField(User, backref='entries')
    slug = CharField(unique=True, max_length=50)
    title = CharField(max_length=100)
    date = DateTimeField()
    time_spent = IntegerField()
    subjects = TextField()
    resources = TextField(null=True)

    class Meta:
        database = DATABASE
        order_by = ('-timestamp',)

    @classmethod
    def get_entries_by_tag(cls, tag):
        """
        Get entries by tags
        """
        entries = Entry.select().join(
            TagEntry, on=TagEntry.entry
        ).where(
            TagEntry.tag == tag
        )
        return entries

    def get_tags(self):
        return Tag.select().join(
            TagEntry, on=TagEntry.tag
        ).where(
            TagEntry.entry == self
        )


class Tag(Model):
    tag = CharField(unique=True, max_length=100)

    class Meta:
        database = DATABASE

    @classmethod
    def create_tag_if_not_exists(cls, tag):
        """
        Create a tag if not exists
        """
        if Tag.get_or_none(Tag.tag == tag) is None:
            Tag.create(
                tag=tag
            )


class TagEntry(Model):
    """
    Tag - Entry relationship model
    """
    tag = ForeignKeyField(Tag, backref='tags')
    entry = ForeignKeyField(Entry, backref='entries')

    class Meta:
        database = DATABASE
        indexes = (
            (('entry', 'tag'), True),
        )

    @classmethod
    def create_tagentry_if_not_exists(cls, tag_id, entry_id):
        """
        Prevent duplicate entries
        """
        if TagEntry.get_or_none(TagEntry.tag_id == tag_id,
                                TagEntry.entry_id == entry_id) is None:
            TagEntry.create(
                tag_id=tag_id,
                entry_id=entry_id
            )


def initialize():
    DATABASE.connect()
    DATABASE.create_tables([User, Entry, Tag, TagEntry], safe=True)
    DATABASE.close()
