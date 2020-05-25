import sqlite3
from sqlite3 import Error
import threading


class Sqlite:

    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = self.connect()

    def connect(self):
        conn = None
        try:
            print("connection to ", self.db_file)
            conn = sqlite3.connect(self.db_file)
        except Error as e:
            print(e, self.db_file)
        return conn

    def add(self, table, val):
        conn = self.conn
        if conn is not None:
            sql = ''' DELETE from ''' + table + ''' WHERE my_time <
                datetime('now', '-1 minute') '''
            conn.execute(sql)
            conn.commit()
            sql = ''' INSERT INTO ''' + table + '''(value,my_time)
                VALUES(?,datetime('now')) '''
            conn.execute(sql, [val])
            conn.commit()


