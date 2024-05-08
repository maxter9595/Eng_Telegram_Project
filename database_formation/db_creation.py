import csv
import os

import sqlalchemy as sq
from psycopg2 import errors
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from sqlalchemy_utils import database_exists, create_database

from database_formation.table_structure import get_table_list, form_tables, Pos, Words


class Database:

    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def write_dir(self, *args) -> os.path:
        abspath = os.path.abspath(args[0])
        root_dir = ''

        for arg in args[1:]:
            if root_dir:
                root_dir = os.path.join(root_dir, arg)
            else:
                root_dir = os.path.join(abspath, arg)

        return root_dir

    def get_engine(self):
        dns_link = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        return create_engine(dns_link)

    def exists_db(self):
        engine = self.get_engine()
        if not database_exists(engine.url):
            return False
        else:
            return True

    def create_db(self):
        engine = self.get_engine()
        if not self.exists_db():
            create_database(engine.url)

    def exists_tables(self):
        engine = self.get_engine()
        table_list = get_table_list()
        for table_name in table_list:
            if not sq.inspect(engine).has_table(table_name):
                return False
        return True

    def create_tables(self):
        engine = self.get_engine()
        if not self.exists_tables():
            form_tables(engine)

    def prepare_pos(self):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        pos_count = session.query(Pos).count()
        if pos_count == 0:
            noun = Pos(id=1, pos_name='noun')
            verb = Pos(id=2, pos_name='verb')
            adjective = Pos(id=3, pos_name='adjective')
            unidentified = Pos(id=4, pos_name='unidentified')
            session.add_all([noun, verb, adjective, unidentified])
            session.commit()
        session.close()

    def get_pos(self):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()
        existing_pos = session.query(Pos).all()
        pos_list = []
        if existing_pos:
            for pos_item in existing_pos:
                pos_list.append({
                    'id': pos_item.id,
                    'pos_name': pos_item.pos_name
                })
            return pos_list

    def prepare_words(self):
        csv_path = self.write_dir('data', 'database_csv', 'database.csv')
        csv_path = csv_path.replace('database_formation/', '')
        with (open(csv_path) as f):
            csv_reader = csv.reader(f)
            data = list(csv_reader)
        self.prepare_pos()
        pos_data = self.get_pos()
        if pos_data:
            object_list = []
            for idx, word_dict in enumerate(data[1:]):
                id_pos = [dict_.get('id') for dict_ in pos_data
                          if dict_.get('pos_name') == word_dict[1]].pop()
                object_list.append(
                    Words(
                        id=idx+1,
                        en_word=word_dict[0],
                        en_trans=word_dict[5],
                        mp_3_url=word_dict[3],
                        id_pos=id_pos,
                        ru_word=word_dict[4],
                        en_example=word_dict[6],
                        ru_example=word_dict[7],
                        is_added_by_users=False
                    )
                )
            engine = self.get_engine()
            Session = sessionmaker(bind=engine)
            session = Session()
            try:
                session.bulk_save_objects(object_list)
                session.commit()
            except (exc.IntegrityError, errors.UniqueViolation):
                pass
            session.close()


if __name__ == '__main__':
    db = Database(dbname='test_db4',
                  user='postgres',
                  password='postgres')
    db.create_db()
    db.create_tables()
    db.prepare_words()