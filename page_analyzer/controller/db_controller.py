import datetime
from urllib.parse import urlparse
from validators import url
import psycopg2
from psycopg2.extras import DictCursor
import os
keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

DATABASE_URL = os.getenv('DATABASE_URL')
def db_connect():
    return psycopg2.connect(DATABASE_URL, **keepalive_kwargs)


class db_work:
    
    def get_all(self):
        con = db_connect()
        SQL = 'SELECT * FROM urls ORDER BY id DESC;'
        with con.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL)
            return [dict(row) for row in cur]
    
    def name_check(self,url):
        con = db_connect()
        SQL = 'SELECT name FROM urls;'
        with con.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(SQL)
                name_dict = cur.fetchall()
        return False if url in name_dict else True
    
    
    def add_url(self, url):
        con = db_connect()
        non_normilized_url = urlparse(url)
        normilized_url = non_normilized_url.scheme + "://" + non_normilized_url.hostname
        if not db_work.name_check(self,normilized_url):
            SQL = 'INSERT INTO urls(name,created_at) VALUES(%s,%s)'
            current_date = datetime.date.today()
            with con.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(SQL, (normilized_url, current_date))
                con.commit()
