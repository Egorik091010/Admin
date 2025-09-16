import sqlite3
from config import DATABASE
con = sqlite3.connect('help.db')
cur = con.cursor()

class DB_Manager:
    def __init__(self, database):
        self.database = database


    def create_tables(self):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.execute('''CREATE TABLE IF NOT EXISTS question(
                        id, 
                        questions TEXT,
                        answers TEXT
                        )''')
            conn.commit()


    def __executemany(self, sql, data):
        conn = sqlite3.connect(self.database)
        with conn:
            conn.executemany(sql, data)
            conn.commit()
    
    def __select_data(self, sql, data = tuple()):
        conn = sqlite3.connect(self.database)
        with conn:
            cur = conn.cursor()
            cur.execute(sql, data)
            return cur.fetchall()
        


con.commit()


if __name__ == '__main__':
    manager = DB_Manager(DATABASE)
    manager.create_tables()  

