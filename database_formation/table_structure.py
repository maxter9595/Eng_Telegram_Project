import sqlalchemy as sq
from sqlalchemy.orm import declarative_base


Base = declarative_base()


class EngWord(Base):
    
    __tablename__ = 'en_word_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                )
    
    en_word = sq.Column(
                        sq.String(length=350),
                        nullable=False, 
                        unique=True
                    )
    
    en_trans = sq.Column(
                        sq.String(length=350)
                    )
    
    mp_3_url = sq.Column(
                        sq.String(length=350)
                    )


class EngPos(Base):
    
    __tablename__ = 'en_pos_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                )
    
    pos_name = sq.Column(
                        sq.String(length=85), 
                        nullable=False, 
                        unique=True
                    )


class EngLevel(Base):
    
    __tablename__ = 'en_level_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                )
    
    level_code = sq.Column(
                            sq.String(length=15), 
                            nullable=False, 
                            unique=True
                        )
    
    level_name = sq.Column(
                            sq.String(length=150), 
                            nullable=False, 
                            unique=True
                        )


class EngExample(Base):
    
    __tablename__ = 'en_example_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                )
    
    en_example = sq.Column(
                            sq.String(length=1500), 
                            nullable=False
                        )
    
    ru_example = sq.Column(
                            sq.String(length=1500), 
                            nullable=False
                        )


class RuWord(Base):
    
    __tablename__ = 'ru_word_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                    )
    
    ru_word = sq.Column(
                        sq.String(length=350), 
                        nullable=False, 
                        unique=True
                    )


class EngDbTable(Base):
    
    __tablename__ = 'en_db_table'
    
    id = sq.Column(
                    sq.Integer, 
                    primary_key=True
                )
    
    id_en_word = sq.Column(
                            sq.Integer, 
                            sq.ForeignKey('en_word_table.id'),
                            nullable=False
                        )
    
    id_pos = sq.Column(
                        sq.Integer, 
                        sq.ForeignKey('en_pos_table.id'), 
                        nullable=False
                    )
    
    id_example = sq.Column(
                            sq.Integer, 
                            sq.ForeignKey('en_example_table.id'),
                            nullable=False
                        )
    
    id_level = sq.Column(
                        sq.Integer, 
                        sq.ForeignKey('en_level_table.id'), 
                        nullable=False
                    )
    
    id_ru_word = sq.Column(
                            sq.Integer, 
                            sq.ForeignKey('ru_word_table.id'), 
                            nullable=False
                        )


def create_tables(engine: sq.Engine) -> None:    
    Base.metadata.create_all(engine)