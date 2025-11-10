import datetime
from urllib.parse import urlparse
from validators import url
import psycopg2
from psycopg2.extras import DictCursor
import os
from itertools import chain
keepalive_kwargs = {
    "keepalives": 1,
    "keepalives_idle": 30,
    "keepalives_interval": 5,
    "keepalives_count": 5,
}

DATABASE_URL = os.getenv('DATABASE_URL')
def db_connect():
    return psycopg2.connect(DATABASE_URL, **keepalive_kwargs)


def validator(new_url):
    if not url(new_url):
        return False
    non_normilized_url = urlparse(new_url)
    normilized_url = non_normilized_url.scheme + "://" + non_normilized_url.hostname
    return normilized_url



class db_work:
    
    def get_all(self):
        con = db_connect()
        SQL = 'SELECT DISTINCT urls.id,urls.name, url_checks.created_at,url_checks.status_code FROM urls LEFT JOIN url_checks ON urls.id = url_checks.url_id AND url_checks.created_at = (SELECT MAX(created_at) FROM url_checks AS uc WHERE uc.url_id = urls.id)ORDER BY urls.id DESC;'
        with con.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL)
            return [dict(row) for row in cur]
    
    def name_check(self,url):
        con = db_connect()
        SQL = 'SELECT name FROM urls;'
        with con.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL)
            name_dict = cur.fetchall()
        return False if url in list(chain.from_iterable(name_dict)) else True
        
    
    def get_by_id(self,id):
        con = db_connect()
        SQL = "SELECT * FROM urls where id = %s;"
        with con.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(SQL,(id,))
                result  = cur.fetchone()
                return dict(result)
    
    def get_last_id(self):
        con = db_connect()
        SQL = "SELECT id FROM urls ORDER BY id DESC"
        with con.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(SQL,(id,))
                result  = cur.fetchone()
                return dict(result)
        
    def add_url(self, normilized_url):
        con = db_connect()
        SQL = 'INSERT INTO urls(name,created_at) VALUES(%s,%s)'
        current_date = datetime.date.today()
        with con.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL, (normilized_url, current_date))
            con.commit()
    


    def add_url_check(self,url_id,status):
        con = db_connect()
        SQL ='INSERT INTO url_checks(url_id,created_at,status_code) VALUES(%s,%s,%s)'
        current_date = datetime.date.today()
        with con.cursor(cursor_factory=DictCursor) as cur:
            cur.execute(SQL, (url_id, current_date,status))
            con.commit()


    def get_by_name(self, name):
        con = db_connect()
        SQL = "SELECT * FROM urls where name = %s ;"
        with con.cursor(cursor_factory=DictCursor) as cur:
                print(name)
                cur.execute(SQL, (name,))
                result  = cur.fetchone()
                return dict(result)
    
    def get_url_cheks(self,id):
        con = db_connect()
        SQL = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC"
        with con.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(SQL,(id,))
                return [dict(row) for row in cur]






# r = requests.get('https://requests.readthedocs.io/en/latest/user/install/#install') # СОЗДАЁТ ОБЪЕКТ РЕСПОНС С КОТОРОГО МОЖНО ВЫТАСКИВАТЬ ГОВНО УРА
# print(type(r.text))  #ЭТА ХУЙНЯ ВОЗВРАЩАЕТ ХТМЛ УРА БЛЯТЬ
