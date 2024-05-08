import sys
import inspect

import sqlalchemy as sq
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Pos(Base):
    __tablename__ = 'pos'

    id = sq.Column(
        sq.Integer,
        primary_key=True
    )

    pos_name = sq.Column(
        sq.String(length=85),
        nullable=False,
        unique=True
    )


class Words(Base):
    __tablename__ = 'words'

    id = sq.Column(
        sq.Integer,
        primary_key=True
    )

    en_word = sq.Column(
        sq.String(length=350),
        nullable=False
    )

    en_trans = sq.Column(
        sq.String(length=350)
    )

    mp_3_url = sq.Column(
        sq.String(length=350)
    )

    id_pos = sq.Column(
        sq.Integer,
        sq.ForeignKey('pos.id'),
        nullable=False
    )

    ru_word = sq.Column(
        sq.String(length=350),
        nullable=False
    )

    en_example = sq.Column(
        sq.String(length=1500),
        nullable=False
    )

    ru_example = sq.Column(
        sq.String(length=1500),
        nullable=False
    )

    is_added_by_users = sq.Column(
        sq.Boolean(),
        nullable=False
    )


class Users(Base):
    __tablename__ = 'users'

    user_id = sq.Column(
        sq.Integer,
        primary_key=True
    )

    first_name = sq.Column(
        sq.String(length=85),
        nullable=False
    )

    last_name = sq.Column(
        sq.String(length=85),
        nullable=False
    )

    username = sq.Column(
        sq.String(length=85),
        nullable=False,
        unique=True
    )


class UsersWords(Base):
    __tablename__ = 'users_words'

    id = sq.Column(
        sq.Integer,
        primary_key=True
    )

    user_id = sq.Column(
        sq.Integer,
        sq.ForeignKey('users.user_id',
                      ondelete='CASCADE'),
        nullable=False
    )

    word_id = sq.Column(
        sq.Integer,
        sq.ForeignKey('words.id'),
        nullable=False,
    )

    is_added = sq.Column(
        sq.Boolean,
        nullable=False
    )

    is_user_word = sq.Column(
        sq.Boolean,
        nullable=False
    )

    date_added = sq.Column(
        sq.DateTime
    )

    date_deleted = sq.Column(
        sq.DateTime
    )


def form_tables(engine: sq.Engine) -> None:
    Base.metadata.create_all(engine)


def get_table_list() -> list:
    table_list = []
    for table_name, obj in inspect.getmembers(sys.modules[__name__]):
        if inspect.isclass(obj):
            if table_name != 'Base':
                table_list.append(obj.__table__.name)
    return table_list
