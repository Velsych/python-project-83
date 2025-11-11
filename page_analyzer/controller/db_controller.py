import psycopg2
from psycopg2.extras import DictCursor
from itertools import chain




class DbManager:
    def __init__(self,db_url):
        self.url = db_url
    
#  add_url  add_url_check
    def fetchall(self,query,*args,**kwargs):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(query,*args,**kwargs)
                return cur.fetchall()
    def fetchone(self,query,*args,**kwargs):
        with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute(query,*args,**kwargs)
                    return cur.fetchone()
    def execute_and_save(self,query,*args,**kwargs):
         with psycopg2.connect(self.url) as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                    cur.execute(query,*args,**kwargs)
                    conn.commit()


class UrlRepository:
    def __init__(self,db_manager):
          self.db_manager = db_manager
    
    def get_all(self):
        SQL = """SELECT DISTINCT 
                urls.id,
                urls.name, 
                url_checks.created_at,
                url_checks.status_code 
                FROM urls 
                LEFT JOIN url_checks ON urls.id = url_checks.url_id 
                AND url_checks.created_at = (
                SELECT MAX(created_at) 
                FROM url_checks AS uc 
                WHERE uc.url_id = urls.id)
                ORDER BY urls.id DESC;"""
        return self.db_manager.fetchall(SQL)
    
    def get_url_checks(self,url_id):
        SQL = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;"
        return self.db_manager.fetchall(SQL,(url_id,))
    

    def get_by_id(self,url_id):
         SQL ="SELECT * FROM urls where id = %s;"
         return self.db_manager.fetchone(SQL,(url_id,))


    def get_last_id(self):
         SQL = 'SELECT id FROM urls ORDER BY id DESC'
         return self.db_manager.fetchone(SQL)
    
    def get_by_name(self,name):
         SQL = 'SELECT * FROM urls where name = %s ;'
         return self.db_manager.fetchone(SQL,(name,))


    def add_url(self,normilized_url,current_date):
         SQL = 'INSERT INTO urls(name,created_at) VALUES(%s,%s)'
         return self.db_manager.execute_and_save(SQL,(normilized_url,current_date))
    
    def add_url_check(self,url_id,created_at,status_code,h1="",title="",description=""):
         SQL ='INSERT INTO url_checks(url_id,status_code,created_at,h1,title,description) VALUES(%s,%s,%s,%s,%s,%s)'
         return self.db_manager.execute_and_save(SQL,(url_id,status_code,created_at,h1,title,description))

    def name_check(self,url):
         SQL = 'SELECT name FROM urls;'
         names = self.db_manager.fetchall(SQL)
         return False if url in list(chain.from_iterable(names)) else True
    




