__author__ = 'JoshOY'

import sys
import json
import MySQLdb

reload(sys)
sys.setdefaultencoding('utf-8')


class MysqlLinker:
    def __init__(self):
        self.db = None
        pass

    def __connect_db(self):
        with open("constants.json") as jsonf:
            dbinfo = json.loads(jsonf.read())[u"dbConnection"]
            db = MySQLdb.connect(dbinfo[u'dbIp'], dbinfo[u'userName'], dbinfo[u'password'], dbinfo[u'dbName'])
            return db

    def __disconnect_db(self):
        if self.db:
            try:
                self.db.close()
            except Exception as err:
                print err

    def execute_sql(self, sql):
        self.__connect_db()
        cursor = self.db.cursor()
        try:
            cursor.execute(sql)
            self.db.commit()
        except Exception as err:
            print "-*-  SQL EXECUTE FAILED! -*-"
            print err
            print "-*-       LOG END        -*-"
            self.db.rollback()
        self.__disconnect_db()

    def insert_values(self, value_tuple, table):
        if type(value_tuple) == list:
            value_tuple = tuple(value_tuple)
        sql = u"INSERT INTO %s VALUES %s;" % (table, value_tuple)
        try:
            self.execute_sql(sql)
        except Exception as err:
            print err
            return False
        return True

    def select_column(self, column_name, table):
        sql = u'SELECT %s FROM %s;' % (column_name, table)
        try:
            self.execute_sql(sql)
        except Exception as err:
            print err
            return False

if __name__ == '__main__':
    pass