import sqlite3
import datetime

conn = sqlite3.connect("IDdatabase.db")
cursor = conn.cursor()
# create table
cursor.execute("""CREATE TABLE IDs (id integer primary key, programtime text, devicetype integer) """)
conn.commit()
date=str(datetime.datetime.now())
print(date)
cursor.execute("INSERT INTO 'IDs' VALUES('0','{}','0')".format(date[:-7]))
conn.commit()
