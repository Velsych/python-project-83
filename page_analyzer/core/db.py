import psycopg2
from psycopg2.extras import DictCursor


class DbManager:
    def __init__(self, db_url):
        self.url = db_url
    
#  add_url  add_url_check
    def fetchall(self, query, *args, **kwargs):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, *args, **kwargs)
                return cur.fetchall()

    def fetchone(self, query, *args, **kwargs):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, *args, **kwargs)
                return cur.fetchone()

    def execute_and_save(self, query, *args, **kwargs):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query, *args, **kwargs)
                conn.commit()