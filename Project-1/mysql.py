#!/usr/bin/python3

#import mysql.connector
import MySQLdb
import globals
from datetime import datetime

eidDB = MySQLdb.connect(host="localhost",
                     user="hardyk",
                     passwd="mysql123",
                     database="EID_projectDB"
)

mycur = eidDB.cursor()

#temp_list = []
#humi_list = []
#time_stamp = []

#mycur.execute("DROP TABLE sensor_values")
#mycur.execute("CREATE TABLE sensor_values (id INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY, timestamp VARCHAR(20), temperature FLOAT(20), humidity FLOAT(20))")


class database:

    def add_values_db(self, temperature, humidity, formatted_time):
        insert_query = "INSERT INTO sensor_values (temperature, humidity, timestamp) VALUES (%s, %s, %s)"
        args = (temperature, humidity, formatted_time)
        mycur.execute(insert_query, args)
        eidDB.commit()
        
    def get_values_db(self):
        mycur.execute("SELECT * FROM sensor_values")
        for row in mycur.fetchall() :
                print (row[0], " ", row[1], " ", row[2], " ", row[3])

    def get_last_ten_values(self):
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET 20")
        for row in mycur.fetchall():
                print (row[0], " ", row[1], " ", row[2], " ", row[3])
                
                
    def get_last_ten_temp_values(self, index):
        if index <= 10:
            index = 0
        else:
            index = index - 10
        fetch = (index,)
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET %s", fetch)
        for row in mycur.fetchall():
                print (row[0], " ", row[1], " ", row[2], " ", row[3])
                globals.temp_list.append(row[2])
                globals.time_stamp.append(row[1])
                
    def get_last_ten_humi_values(self, index):
        if index <= 10:
            index = 0
        else:
            index = index - 10
        fetch = (index,)
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET %s", fetch)
        for row in mycur.fetchall():
                print (row[0], " ", row[1], " ", row[2], " ", row[3])
                globals.humi_list.append(row[3])
                globals.time_stamp.append(row[1])

    def delete_values_db(self):
        mycur.execute("DELETE FROM sensor_values")
        eidDB.commit()
        mycur.execute("ALTER TABLE sensor_values AUTO_INCREMENT = 1")


db1 = database()

for i in range(30):
    timestamp = datetime.now()
    formattedtime = timestamp.strftime('%H:%M:%S')
    db1.add_values_db(10.20, 12.21, formattedtime)
    

#globals.global_init()

#db1.get_values_db()
#db1.get_last_ten_values()
#db1.get_last_ten_temp_values(5)
#db1.get_last_ten_humi_values()
#db1.delete_values_db()
#
#plt.plot(temp_list, time_stamp, label='temp', color='red', linewidth=3)
#plt.plot(humi_list, time_stamp, label='humi', color='green', linewidth=3)
#plt.xlabel('x - axis')
#plt.ylabel('y - axis')
#plt.legend()
#plt.title('Graph')
#plt.show()
