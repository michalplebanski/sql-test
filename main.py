import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """create a database connection to a SQLlite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version} ")
    except Error as e:
        print(e)
    
    return conn

def create_connection_in_memory():
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(":memory")
        print(f"Connected, sqlite version: {sqlite3.version}")
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()
        
def execute_sql(conn, sql):
    """ Execute sql
    :param conn: Connection object
    :param sql: a SQL script
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(sql)
    except Error as e:
        print(e)

if __name__ == '__main__':
    create_urls_sql = """
    -- URLS TABLE
    CREATE TABLE IF NOT EXISTS urls (
        id integer PRIMARY KEY,
        nazwa text NOT NULL
    );
    """

    create_meta_sql = """
    --- META TABLE
    CREATE TABLE IF NOT EXISTS meta (
        id integer PRIMARY KEY,
        projekt_id integer NOT NULL,
        meta_title TEXT,
        meta_description TEXT,
        header_1 TEXT,
        FOREIGN KEY (projekt_id) REFERENCES urls (id)
    )
    """

    db_file = "database.db"
    conn = create_connection(db_file)
    if conn is not None:
        execute_sql(conn, create_urls_sql)
        execute_sql(conn, create_meta_sql)
        create_connection_in_memory()
        conn.close()

