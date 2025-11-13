

class UrlRepository:
    def __init__(self, db_manager):
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
    
    def get_url_checks(self, url_id):
        SQL = "SELECT * FROM url_checks WHERE url_id = %s ORDER BY id DESC;"
        return self.db_manager.fetchall(SQL, (url_id,))
    
    def get_by_id(self, url_id):
        SQL = "SELECT * FROM urls where id = %s;"
        return self.db_manager.fetchone(SQL, (url_id,))

    def get_last_id(self):
        SQL = 'SELECT id FROM urls ORDER BY id DESC'
        return self.db_manager.fetchone(SQL)
    
    def get_by_name(self, name):
        SQL = 'SELECT * FROM urls where name = %s ;'
        return self.db_manager.fetchone(SQL, (name,))

    def add_url(self, normilized_url, current_date):
        SQL = 'INSERT INTO urls(name,created_at) VALUES(%s,%s)'
        return self.db_manager.execute_and_save(SQL, (normilized_url,
                                                       current_date))
    
    def add_url_check(self, url_id, created_at,
                       status_code, h1="", title="", description=""):
        SQL = '''INSERT INTO url_checks(url_id,
        status_code,
        created_at,h1,
        title,
        description)
          VALUES(%s,%s,%s,%s,%s,%s)'''
        return self.db_manager.execute_and_save(SQL, (url_id,
                                                       status_code,
                                                        created_at,
                                                        h1,
                                                        title, description))

    def check_name_in_db(self, url):
        SQL = 'SELECT id,name FROM urls WHERE name = %s;'
        name = self.db_manager.fetchone(SQL, (url,))
        print(name)
        if name is None:
            return False, True
        else:
            return name['id'], False
    




