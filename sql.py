from sqlite3 import connect
from datetime import datetime

class Database:

    @staticmethod
    def my_select():
        try:
            my_con = connect("Staff.db")
            my_cursor = my_con.cursor()
            my_cursor.execute("SELECT * FROM personnel")
            result = my_cursor.fetchall()
            my_cursor.close()
            return result
        except:
            return []

    @staticmethod
    def my_delete(code):
        try:
            my_con = connect("Staff.db")
            my_cursor = my_con.cursor()
            my_cursor.execute(f"DELETE FROM personnel WHERE code={code}")
            my_con.commit()
            my_cursor.close()
            return True
        except:
            return False


    @staticmethod
    def my_insert(code,name,family,birth,image):
        try:
            my_con = connect("Staff.db")
            my_cursor = my_con.cursor()
            time='{0:%y-%m-%d}'.format(datetime.now())
            my_cursor.execute(f"INSERT INTO personnel(code,first_name,last_name,birth,image,date)VALUES({code},'{name}','{family}',{birth},'{image}','{time}')")
            # code=my_cursor.lastrowid
            my_con.commit()
            my_cursor.close()
            return True
        except:
            return False