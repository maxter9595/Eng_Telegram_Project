import psycopg2
from psycopg2 import sql


def create_database(db_name:str, user:str, password:str,
                    host:str='localhost') -> None:
    
    try:
        con_config = dict(
                            dbname='postgres', 
                            user=user, 
                            password=password, 
                            host=host
                        )
        
        conn = psycopg2.connect(**con_config)
        conn.autocommit = True
        
        cur = conn.cursor()
        cur.execute(
                    sql.SQL("CREATE DATABASE {}").\
                        format(sql.Identifier(db_name))
                    )
        print(f'База данных {db_name} сформирована')
    
    except psycopg2.errors.DuplicateDatabase:
        print(f'База данных {db_name} уже сформирована')