#!/usr/bin/python3

#Authors: Hardik Senjaliya and Isha Sawant
#This file is for generating a mysqldb and contains all the funtions necessary for plotting the 10-values in the graph


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

#mycur.execute("DROP TABLE sensor_values")
#mycur.execute("CREATE TABLE sensor_values (id INT(20) NOT NULL AUTO_INCREMENT PRIMARY KEY, formatted_time VARCHAR(20), tempc FLOAT(20), tempf FLOAT(20), humidity FLOAT(20))")

class database:

    #add values of temperature and humidity to the database
    def add_values_db(self, tempc, tempf, humidity, formatted_time):
        insert_query = "INSERT INTO sensor_values (tempc, tempf, humidity, formatted_time) VALUES (%s, %s, %s, %s)"
        args = (tempc, tempf, humidity, formatted_time)
        mycur.execute(insert_query, args)
        eidDB.commit()

    #print values once the plot is displayed
    def get_last_ten_values(self):
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET 20")
        for row in mycur.fetchall():
                print (row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4])

    #fetch 10 temp values for the plot
    def get_last_ten_temp_values(self, index):
        if index <= 10:
            index = 0
        else:
            index = index - 10
        fetch = (index,)
        print("Num  Time     T(C)   T(F)")
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET %s", fetch)
        for row in mycur.fetchall():
            print (row[0], " ", row[1], " ", row[2], " ",row[3])
            globals.tempc_list.append(row[2])
            globals.tempf_list.append(row[3])
            globals.time_stamp.append(row[1])

    #fetch 10 humidity values for the plot
    def get_last_ten_humi_values(self, index):
        if index <= 10:
            index = 0
        else:
            index = index - 10
        fetch = (index,)
        mycur.execute("SELECT * FROM sensor_values LIMIT 10 OFFSET %s", fetch)
        print("Num  Time      Humidity ")
        for row in mycur.fetchall():
                print (row[0], " ", row[1], " ", row[4])
                globals.humi_list.append(row[4])
                globals.time_stamp.append(row[1])
                
    #print all values after 30 readings
    def printall(self,index):
        index=0
        fetch = (index,)
        print("=================================================================")
        print("Number  Time     T(C)  T(F)   Humidity ")
        mycur.execute("SELECT * FROM sensor_values LIMIT 30 OFFSET %s", fetch)
        for row in mycur.fetchall():
            print (row[0], " ", row[1], " ", row[2], " ", row[3], " ", row[4])
            globals.tempc_list.append(row[2])
            globals.tempf_list.append(row[3])
            globals.humi_list.append(row[4])
            globals.time_stamp.append(row[1])
        print("=================================================================")

    def delete_values_db(self):
        mycur.execute("DELETE FROM sensor_values")
        eidDB.commit()
        mycur.execute("ALTER TABLE sensor_values AUTO_INCREMENT = 1")

for i in range(30):
    timestamp = datetime.now()
    formattedtime = timestamp.strftime('%H:%M:%S')