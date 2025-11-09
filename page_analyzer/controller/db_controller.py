import datetime
from urllib.parse import urlparse
from validators import url
from psycopg2.extras import DictCursor


class db_work:
    def __init__(self, conn):
        self.conn = conn
    
    def get_all(self):
        SQL = 'SELECT * FROM urls ORDER BY id DESC;'
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL)
            return [dict(row) for row in cur]
    
    def add_url(self, url):
        SQL = 'INSERT INTO urls(name,created_at) VALUES(%s,%s)'
        non_normilized_url = urlparse(url)
        normilized_url = non_normilized_url.scheme + "://" + non_normilized_url.hostname
        current_date = datetime.date.today()
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL, (normilized_url, current_date))
            self.conn.commit()


