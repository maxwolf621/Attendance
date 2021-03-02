import sqlite3
''' 
    record the time of employee's attendence
'''

class dbinsert:
    def __init__(self,time,date,late,empid,dbname):
        self.empid = empid
        self.date = date
        self.time = time
        self.late = late
        self.conn = sqlite3.connect(dbname)
        self.cursor = self.conn.cursor()
        self.shutdown = False
        if self.shutdown :
            self.conn.close()
    def insert(self):
        if not self.check() :
            self.cursor.execute(f"INSERT INTO Record (time,date,late,emp_id) VALUES ('{self.time}' , '{self.date}' , '{self.late}', '{self.empid}')")
            self.conn.commit()
        else:
            print('The Employee has been already done it')
        self.shutdown = True
    def check(self):
        self.cursor.execute(f"SELECT * FROM Record WHERE emp_id = '{self.empid}' and date = '{self.date}' ")
        result = self.cursor.fetchall()
        self.conn.commit()
        return result
a = dbinsert("07:50","2020/6/25",'No',"5157",'site.db')
a.insert()
        
        
        