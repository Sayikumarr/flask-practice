import sqlite3

class Student:
    def __init__(self):
        self.con = sqlite3.connect('Student_details.db')
        self.cur = self.con.cursor()
        self.create_table()
        
    def create_table(self):
        self.cur.execute("""CREATE TABLE IF NOT EXISTS student(
        rollno TEXT PRIMARY KEY,
        f_name TEXT,
        l_name TEXT,
        marks REAL)""")
        
    def insert(self,student):
        self.cur.execute("""INSERT OR IGNORE INTO student VALUES(?,?,?,?)""",student)
        self.con.commit()

    def update(self,student):
        self.cur.execute(f"""UPDATE student SET 
        f_name = '{student[1]}',
        l_name = '{student[2]}',
        marks = '{student[3]}' 
        WHERE rollno = {student[0]}""")
        self.con.commit()
        
    def read(self):
        self.cur.execute("""SELECT * FROM student""")
        records = self.cur.fetchall()
        return records