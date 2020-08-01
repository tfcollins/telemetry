
import sqlite3
from os import path


class db:
    def __init__(self, db_filename='results.db'):
        self.db_filename = db_filename
        self.table_name = "COMPANY"
        if not path.exists(self.db_filename):
            self.conn = sqlite3.connect(self.db_filename)
            self.create_db()
        else:
            self.conn = sqlite3.connect(self.db_filename)

    def create_db(self):
        print("Creating db")
        self.conn.execute('''CREATE TABLE '''+self.table_name+'''
            (ID INT PRIMARY KEY     NOT NULL,
            NAME           TEXT    NOT NULL,
            AGE            INT     NOT NULL,
            ADDRESS        CHAR(50),
            SALARY         REAL);''')
        print("Created db")

    def check_if_exists(self,id):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM "+self.table_name+" WHERE ID=?", (id,))
        rows = cur.fetchall()
        print(rows)
        return len(rows)>0

    def add_entry(self):
        id = 3
        if not self.check_if_exists(id):
            self.conn.execute("INSERT INTO COMPANY (ID,NAME,AGE,ADDRESS,SALARY) \
                    VALUES (3, 'Teddy', 23, 'Norway', 20000.00 )")
            self.conn.commit()
        else:
            print("Entry already exists")

    def print_all(self):
        cursor = self.conn.execute("SELECT id, name, address, salary from COMPANY")
        for row in cursor:
            print("ID = ", row[0])
            print("NAME = ", row[1])
            print("ADDRESS = ", row[2])
            print("SALARY = ", row[3])

    def __del__(self):
        self.conn.close()

if __name__ == "__main__":
    d = db()
    d.add_entry()
    d.print_all()
    del d