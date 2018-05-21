import os.path
import sys
import MySQLdb
from config import ConfigReader


class DbTool(object):

    def open(self):
        cnf = ConfigReader()
        self._connect = MySQLdb.connect(
            host=cnf.get('DB_HOST'), user=cnf.get('DB_USER'), 
            passwd=cnf.get('DB_PASSWORD'), db=cnf.get('DB_NAME'))
        self._cursor = self._connect.cursor() 

    def close(self):
        self._cursor.close()
        self._connect.close()

    def commit(self):
        self._connect.commit()

#--------------get records-------------------#        
    
    def get_industries(self):
        self._call_sp("industry__get")
        return self._finalize_sp(self._cursor.fetchall())

    def get_companies(self):
        self._call_sp("company__get")
        return self._finalize_sp(self._cursor.fetchall())

    def get_pubs(self):
        self._call_sp("pub__get")
        return self._finalize_sp(self._cursor.fetchall())

    def create_pub(self, name):       
        self._call_sp("pub__create", (name,))
        new_id = self._cursor.fetchone()[0]
        return self._finalize_sp(new_id)

    def create_article(self, company_id, pub_id, published, author, headline, body):
        self._call_sp("article__create", (company_id, pub_id, published, author, headline, body))
        new_id = self._cursor.fetchone()[0]
        return self._finalize_sp(new_id)

# ----------------- private -----------------#

    def _call_sp(self, sp, params = None):
        if params is not None:
            self._cursor.callproc(sp, params)
        else:
            self._cursor.callproc(sp)

    def _finalize_sp(self, result):
        self._cursor.nextset() #mysqldb/python requirement
        return result

    def _sp_fetch_one(self, sp, params = None):
        self._call_sp(sp, params)
        return self._finalize_sp(self._cursor.fetchone())
    
    def _sp_fetch_all(self, sp, params = None):
        self._call_sp(sp, params)
        return self._finalize_sp(self._cursor.fetchall())
        self._cursor.nextset() #mysqldb/python requirement

    def _exec_lastrowid(self, sql, params):
        self._cursor.execute(sql, params)
       return self._cursor.lastrowid
