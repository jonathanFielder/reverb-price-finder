import sqlite3 as lite

class Data_Base:
    
    def __init__(self, db):
        self.db = db
        self.connect()

    def connect(self):
        self.conn = lite.connect(self.db)
        self.cursor = self.conn.cursor()
        self.connected = True

    def commit(self):
        self.conn.commit()

    def close(self):
        self.conn.commit()
        self.conn.close()
        self.connected = False

    def c_ex(self, sql):#cursor execute
        self.cursor.execute(sql)

    def c_ex_it(self, sql_add_q, items):#cursor execute items
        self.cursor.execute(sql_add_q, items)

    def query_all(self, table):
#query database | * means everything
        self.cursor.execute("SELECT * FROM {}".format(table))
        self.result = self.cursor.fetchall()
        return self.result

    def query(self, query):
        try:
            self.cursor.execute(query)
            self.result = self.cursor.fetchall()
        except:
            print('error expecting query. check format')
            return None
        else:
            return self.result






def main():
    pass


if __name__ == '__main__':
    main()
