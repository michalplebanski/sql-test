import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """create a database connection to a SQLlite database"""
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(f"Connected to {db_file}, sqlite version: {sqlite3.version} ")
        return conn
    except Error as e:
        print(e)
    
    return conn
        
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

def add_urls(conn, urls):
    """
    Create a new record into the URLS table
    :param conn:
    :param project:
    """
    sql = '''INSERT INTO urls(nazwa) VALUES(?)'''
    cur = conn.cursor()
    cur.execute(sql, urls)
    return cur.lastrowid

def add_meta(conn, meta):
    """
    Create a new record into the META table
    :param conn:
    :param meta:
    """
    sql = '''INSERT INTO meta(id, projekt_id, meta_title, meta_description, header_1) VALUES(?,?,?,?,?)'''
    cur = conn.cursor()
    cur.execute(sql, meta)
    return cur.lastrowid

def select_meta_by_id(conn, id):
    """
    Query tasks by priority
    :param conn: the Connection object
    :param id
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT * FROM meta WHERE id=?", (str(id)))

    rows = cur.fetchall()
    return rows

def update(conn, table, id, meta_title):
    """
    Update meta title
    :param conn: the Connection object
    :param table: table name
    :id:
    :meta_title
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"UPDATE {table} SET meta_title = '{meta_title}' WHERE id = {id}")
    conn.commit()

def delete(conn, table, id):
    """
    Delete specific record
    :param conn: the Connection object
    :param table: table name
    :id:
    :return:
    """
    cur = conn.cursor()
    cur.execute(f"DELETE FROM {table} WHERE id = {id}")
    conn.commit()

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
    execute_sql(conn, create_urls_sql)
    execute_sql(conn, create_meta_sql)
    urls = ("widoczni.pl",)
    urls_2 = ("widzialni.pl",)
    pr_id = add_urls(conn, urls)
    meta = (
        pr_id,
        "Widoczni",
        "Pozycjonowanie stron",
        "Zapraszamy do najlepszej agancji",
        "Pozycjonowanie"
    )
    add_meta(conn, meta)
    print(select_meta_by_id(conn, 1))
    update(conn, "meta", 1, "Widzialni")
    add_urls(conn, urls_2)
    delete(conn, "urls", id=2)
    conn.commit()
    conn.close()