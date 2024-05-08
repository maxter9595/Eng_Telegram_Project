import datetime

from psycopg2 import errors
from sqlalchemy import create_engine, exc
from sqlalchemy.orm import sessionmaker
from database_formation.table_structure import Pos, Users, Words, UsersWords


class Repository:

    def __init__(self, dbname, user, password, host='localhost', port='5432'):
        self.dbname = dbname
        self.user = user
        self.password = password
        self.host = host
        self.port = port

    def get_engine(self):
        dns_link = f"postgresql://{self.user}:{self.password}@{self.host}:{self.port}/{self.dbname}"
        return create_engine(dns_link)

    def add_pos(self, pos_name):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_pos = session.query(Pos). \
            filter_by(pos_name=pos_name). \
            first()

        if not existing_pos:
            last_pos = session.query(Pos). \
                order_by(Pos.id.desc()). \
                first()

            if not last_pos:
                new_id = 1
            else:
                new_id = last_pos.id + 1

            new_pos = Pos(
                id=new_id,
                pos_name=pos_name
            )

            session.add(new_pos)
            session.commit()

        session.close()

    def update_pos(self, existing_pos_name, new_pos_name):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_pos = session.query(Pos). \
            filter_by(pos_name=existing_pos_name). \
            first()

        new_pos = session.query(Pos). \
            filter_by(pos_name=new_pos_name). \
            first()

        if existing_pos and not new_pos:
            existing_pos.id = existing_pos.id
            existing_pos.pos_name = new_pos_name

            session.commit()

        session.close()

    def delete_pos(self, pos_name):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_pos = session.query(Pos). \
            filter_by(pos_name=pos_name). \
            first()

        if existing_pos:
            session.delete(existing_pos)
            session.commit()

        session.close()

    def get_pos(self):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_pos = session.query(Pos).all()
        session.close()

        if existing_pos:
            pos_list = []
            for pos_item in existing_pos:
                pos_list.append({
                    'id': pos_item.id,
                    'pos_name': pos_item.pos_name
                })
            return pos_list
        else:
            return []

    def add_word(self, data_dict, is_added_by_users):
        pos_list = self.get_pos()
        pos_name = data_dict.get('pos_name')

        if pos_list:
            id_pos = []
            for pos_dict in pos_list:
                if pos_dict.get('pos_name') == pos_name:
                    id_pos.append(pos_dict.get('id'))

            if id_pos:
                id_pos = id_pos.pop()
                en_word = data_dict.get('en_word')
                en_trans = data_dict.get('en_trans')
                mp_3_url = data_dict.get('mp_3_url')
                ru_word = data_dict.get('ru_word')
                en_example = data_dict.get('en_example')
                ru_example = data_dict.get('ru_example')

                engine = self.get_engine()
                Session = sessionmaker(bind=engine)
                session = Session()

                existing_word = session.query(Words). \
                    filter_by(en_word=en_word, id_pos=id_pos). \
                    first()

                if not existing_word:
                    last_word = session.query(Words). \
                        order_by(Words.id.desc()). \
                        first()

                    if not last_word:
                        new_id = 1
                    else:
                        new_id = last_word.id + 1

                    new_word = Words(
                        id=new_id,
                        en_word=en_word,
                        en_trans=en_trans,
                        mp_3_url=mp_3_url,
                        id_pos=id_pos,
                        ru_word=ru_word,
                        en_example=en_example,
                        ru_example=ru_example,
                        is_added_by_users=is_added_by_users
                    )

                    session.add(new_word)
                    session.commit()

                else:
                    existing_word.en_trans = en_trans
                    existing_word.mp_3_url = mp_3_url
                    existing_word.ru_word = ru_word
                    existing_word.en_example = en_example
                    existing_word.ru_example = ru_example
                    existing_word.is_added_by_users = is_added_by_users
                    session.commit()

                session.close()

    def delete_word(self, data_dict):
        pos_list = self.get_pos()
        pos_name = data_dict.get('pos_name')

        if pos_list:
            id_pos = []
            for pos_dict in pos_list:
                if pos_dict.get('pos_name') == pos_name:
                    id_pos.append(pos_dict.get('id'))

            if id_pos:
                id_pos = id_pos.pop()
                en_word = data_dict.get('en_word')

                engine = self.get_engine()
                Session = sessionmaker(bind=engine)
                session = Session()

                existing_word = session.query(Words). \
                    filter_by(en_word=en_word,
                              id_pos=id_pos). \
                    first()

                if existing_word:
                    session.delete(existing_word)
                    session.commit()

                session.close()

    def get_words(self, en_word=None, is_added_by_users=False):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        if not en_word:
            existing_words = session.query(Words). \
                filter_by(is_added_by_users=is_added_by_users). \
                all()
        else:
            existing_words = session.query(Words). \
                filter_by(en_word=en_word,
                          is_added_by_users=is_added_by_users). \
                all()

        session.close()

        if existing_words:
            words_list = []
            for word_item in existing_words:
                words_list.append({
                    'id': word_item.id,
                    'en_word': word_item.en_word,
                    'en_trans': word_item.en_trans,
                    'mp_3_url': word_item.mp_3_url,
                    'id_pos': word_item.id_pos,
                    'ru_word': word_item.ru_word,
                    'en_example': word_item.en_example,
                    'ru_example': word_item.ru_example,
                    'is_added_by_users': word_item.is_added_by_users,
                })
            return words_list
        else:
            return []

    def add_user(self, user_dict):
        user_id = user_dict.get('user_id')
        first_name = user_dict.get('first_name')
        last_name = user_dict.get('last_name')
        username = user_dict.get('username')

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_user = session.query(Users). \
            filter_by(user_id=user_id). \
            first()

        if not existing_user:
            new_user = Users(
                user_id=user_id,
                first_name=first_name,
                last_name=last_name,
                username=username
            )
            session.add(new_user)
            session.commit()

        else:
            existing_user.first_name = first_name
            existing_user.last_name = last_name
            existing_user.username = username
            session.commit()

        session.close()

    def delete_user(self, user_id):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_user = session.query(Users). \
            filter_by(user_id=user_id). \
            first()

        if existing_user:
            session.delete(existing_user)
            session.commit()

        session.close()

    def get_users(self, user_id=None):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        if not user_id:
            existing_users = session.query(Users). \
                all()
        else:
            existing_users = session.query(Users). \
                filter_by(user_id=user_id). \
                all()

        session.close()

        if existing_users:
            users_list = []
            for user_item in existing_users:
                users_list.append({
                    'user_id': user_item.user_id,
                    'first_name': user_item.first_name,
                    'last_name': user_item.last_name,
                    'username': user_item.username
                })
            return users_list
        else:
            return []

    def prepare_user_word_pairs(self, user_id):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        word_data = self.get_words()
        user_data = self.get_users(user_id=user_id)

        words_id = []
        if word_data:
            for word_dict in word_data:
                words_id.append(word_dict.get('id'))

        user_id = 0
        if user_data:
            user_id += user_data.pop().get('user_id')

        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        existing_user = session.query(UsersWords). \
            filter_by(user_id=user_id). \
            first()

        session.close()

        if not existing_user and words_id and user_id:

            engine = self.get_engine()
            Session = sessionmaker(bind=engine)
            session = Session()

            last_user_word_pair = session.query(UsersWords). \
                order_by(UsersWords.id.desc()). \
                first()

            session.close()

            if last_user_word_pair:
                idx_start = last_user_word_pair.id
            else:
                idx_start = 0

            object_list = []
            for idx, word_id in enumerate(words_id):
                object_list.append(
                    UsersWords(
                        id=idx_start + (idx + 1),
                        user_id=user_id,
                        word_id=word_id,
                        is_added=True,
                        is_user_word=False,
                        date_added=datetime.datetime.now(),
                        date_deleted=None
                    )
                )

            engine = self.get_engine()
            Session = sessionmaker(bind=engine)
            session = Session()

            try:
                session.bulk_save_objects(object_list)
                session.commit()
            except (exc.IntegrityError, errors.UniqueViolation) as e:
                pass

            session.close()

    def add_user_word(self, user_id, data_dict):
        word_data = self.get_words(en_word=data_dict.get('en_word'))
        user_data = self.get_users(user_id=user_id)

        if user_data:
            if not word_data:
                self.add_word(
                    data_dict,
                    is_added_by_users=True
                )
                word_data = self.get_words(
                    en_word=data_dict.get('en_word'),
                    is_added_by_users=True
                )

            words_id = []
            for dict_word in word_data:
                words_id.append(dict_word.get('id'))

            if words_id:

                engine = self.get_engine()
                Session = sessionmaker(bind=engine)
                session = Session()

                last_user_word_pair = session.query(UsersWords). \
                    order_by(UsersWords.id.desc()). \
                    first()

                session.close()

                if last_user_word_pair:
                    idx_start = last_user_word_pair.id
                else:
                    idx_start = 0

                object_list = []
                for idx, word_id in enumerate(words_id):
                    engine = self.get_engine()
                    Session = sessionmaker(bind=engine)
                    session = Session()

                    existing_word_user_pair = session.query(UsersWords). \
                        filter_by(user_id=user_id, word_id=word_id). \
                        first()

                    if not existing_word_user_pair:
                        object_list.append(
                            UsersWords(
                                id=idx_start + (idx + 1),
                                user_id=user_id,
                                word_id=word_id,
                                is_added=True,
                                is_user_word=True,
                                date_added=datetime.datetime.now(),
                                date_deleted=None
                            )
                        )

                    else:
                        if existing_word_user_pair.is_added is not True:
                            existing_word_user_pair.is_added = True
                            existing_word_user_pair.date_added = datetime.datetime.now()
                            existing_word_user_pair.date_deleted = None
                            session.commit()

                    session.close()

                if object_list:
                    engine = self.get_engine()
                    Session = sessionmaker(bind=engine)
                    session = Session()

                    try:
                        session.bulk_save_objects(object_list)
                        session.commit()
                    except (exc.IntegrityError, errors.UniqueViolation) as e:
                        print(e)
                        pass

                    session.close()

    def remove_user_word(self, user_id, en_word):
        word_data1 = self.get_words(en_word, is_added_by_users=False)
        word_data2 = self.get_words(en_word, is_added_by_users=True)
        word_data = word_data1 + word_data2

        if word_data:
            for dict_data in word_data:
                word_id = dict_data.get('id')

                engine = self.get_engine()
                Session = sessionmaker(bind=engine)
                session = Session()

                existing_word_user_pair = session.query(UsersWords). \
                    filter_by(user_id=user_id, word_id=word_id, is_added=True). \
                    first()

                if existing_word_user_pair:
                    existing_word_user_pair.is_added = False
                    existing_word_user_pair.date_added = None
                    existing_word_user_pair.date_deleted = datetime.datetime.now()
                    session.commit()

                session.close()

    def delete_user_word_pair(self, user_id, en_word):
        word_data1 = self.get_words(en_word, is_added_by_users=False)
        word_data2 = self.get_words(en_word, is_added_by_users=True)
        word_data = word_data1 + word_data2

        if word_data:
            for dict_data in word_data:
                word_id = dict_data.get('id')

                engine = self.get_engine()
                Session = sessionmaker(bind=engine)
                session = Session()

                existing_word_user_pair = session.query(UsersWords). \
                    filter_by(user_id=user_id, word_id=word_id). \
                    first()

                if existing_word_user_pair:
                    session.delete(existing_word_user_pair)
                    session.commit()

                session.close()

    # def remove_user_word(self, user_id, en_word):
    #     word_data1 = self.get_words(en_word, is_added_by_users=False)
    #     word_data2 = self.get_words(en_word, is_added_by_users=True)
    #     word_data = word_data1 + word_data2
    #
    #     if word_data:
    #         for dict_data in word_data:
    #             word_id = dict_data.get('id')
    #
    #             engine = self.get_engine()
    #             Session = sessionmaker(bind=engine)
    #             session = Session()
    #
    #             existing_word_user_pair = session.query(UsersWords). \
    #                 filter_by(user_id=user_id, word_id=word_id, is_added=True). \
    #                 first()
    #
    #             if existing_word_user_pair:
    #                 existing_word_user_pair.is_added = False
    #                 existing_word_user_pair.date_added = None
    #                 existing_word_user_pair.date_deleted = datetime.datetime.now()
    #                 session.commit()
    #
    #             session.close()





    def get_user_words(self, user_id):
        engine = self.get_engine()
        Session = sessionmaker(bind=engine)
        session = Session()

        query_result = session.query(Words, UsersWords, Users, Pos). \
            join(UsersWords, UsersWords.word_id == Words.id). \
            join(Users, Users.user_id == UsersWords.user_id). \
            join(Pos, Pos.id == Words.id_pos). \
            filter(UsersWords.user_id == user_id, UsersWords.is_added == True). \
            all()

        if query_result:
            user_words_list = []
            for word, user_word, user, pos in query_result:
                user_words_list.append({
                    'en_word': word.en_word,
                    'en_trans': word.en_trans,
                    'mp_3_url': word.mp_3_url,
                    'pos_name': pos.pos_name,
                    'ru_word': word.ru_word,
                    'en_example': word.en_example,
                    'ru_example': word.ru_example
                })
            return user_words_list
        else:
            return []





if __name__ == '__main__':
    rep = Repository(dbname='test_db4',
                     user='postgres',
                     password='postgres')

    # user_dict = {
    #     'user_id': 111111,
    #     'first_name': 'Max',
    #     'last_name': 'Telet',
    #     'username': 'wkeokmoem'
    # }
    #
    # user_dict2 = {
    #     'user_id': 1111112,
    #     'first_name': 'Max2',
    #     'last_name': 'Telet2',
    #     'username': 'wkeokmoem2'
    # }
    #
    # rep.add_user(user_dict)
    # rep.add_user(user_dict2)
    #
    # rep.prepare_user_word_pairs(111111)
    # rep.prepare_user_word_pairs(1111112)
    #
    # rep.prepare_user_word_pairs(111113313)
    #
    # data_dict = {
    #     'en_word': 'new word',
    #     'en_trans': 'trans1010101',
    #     'mp_3_url': 'mp1010101',
    #     'pos_name': 'noun',
    #     'ru_word': 'ru_word1010101',
    #     'en_example': 'en_example1010101',
    #     'ru_example': 'ru_example1010101'
    # }
    #
    # rep.add_user_word(user_id=111111, data_dict=data_dict)
    # rep.add_user_word(user_id=1111112, data_dict=data_dict)
    #
    # rep.remove_user_word(user_id=1111112, en_word='new word')
    # print(rep.get_user_words(1111112))
