import sqlalchemy as sq
from sqlalchemy.orm import sessionmaker

from database_formation.table_structure import EngWord, EngPos
from database_formation.table_structure import EngLevel, EngExample
from database_formation.table_structure import RuWord, EngDbTable


def get_db_table(db_name:str, user:str, 
                password:str, host: str = 'localhost', 
                port: str = '5432') -> list:
    
    DSN = f"postgresql://{user}:{password}@{host}:{port}/{db_name}"
    engine = sq.create_engine(DSN)
    
    session_class = sessionmaker(bind=engine)
    session = session_class()
    
    query = session.\
            query(EngDbTable, EngWord, EngPos, EngLevel, EngExample, RuWord).\
            join(EngWord, EngWord.id ==  EngDbTable.id_en_word).\
            join(EngPos, EngPos.id == EngDbTable.id_pos).\
            join(EngLevel, EngLevel.id == EngDbTable.id_level).\
            join(EngExample, EngExample.id == EngDbTable.id_example).\
            join(RuWord, RuWord.id == EngDbTable.id_ru_word)

    english_data = []
    
    for en_db, en_word, en_pos, en_lvl, example, ru_word in query:
        
        english_data.append({
                            'id': en_db.id,
                            'en_word': en_word.en_word,
                            'en_trans': en_word.en_trans,
                            'mp_3_url': en_word.mp_3_url,
                            'pos_name': en_pos.pos_name,
                            'en_lvl_code': en_lvl.level_code,
                            'en_lvl_name': en_lvl.level_name,
                            'en_example': example.en_example,
                            'ru_example': example.ru_example,
                            'ru_word': ru_word.ru_word
                        })

    session.commit()
    session.close()
    
    return english_data