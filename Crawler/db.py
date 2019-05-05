
import pymysql
DB_HOST = '47.106.110.50'
DB_PORT = 14000
DB_USER='Fijon'
DB_PWD = 'sql_FIJON_920630'
DB_DB = 'stock' 

class SQLOperation():
    
    def __init__(self):
        self.db =  pymysql.connect(host = DB_HOST, user= DB_USER, passwd=DB_PWD,db= DB_DB, port=DB_PORT)
        self.cursor = self.db.cursor()
    
    def insert_into(self, sql):       
        try:
            # 执行sql语句
            self.cursor.execute(sql)
            # 执行sql语句
            self.db.commit()
        except Exception as  e:
            # 发生错误时回滚
            print(sql)
            print(e)
            self.db.rollback()
    
    def select(self, sql):
        self.cursor.execute(sql)
        result = self.cursor.fetchall()
        return result
        