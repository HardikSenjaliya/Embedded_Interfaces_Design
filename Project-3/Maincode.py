#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Project1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

#Authors: Isha Sawant and Hardik Senjaliya
#This .py file is generated from the UI and programmed as the driver class of the code

#files and libraries to be included

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtCore import pyqtSlot
import Adafruit_DHT
from datetime import date, datetime
from time import sleep
import threading
from mplwidget import MplWidget
from mysql import database
import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import asyncio
import socket
import MySQLdb
import Adafruit_DHT
import globals
import sys
import os
import MySQLdb
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json

#global variables

tempunit = "C"
count = 0
humidity = 0.0
temperature = 0.0
disconnectflag=0
tempc = 0.0
tempf = 0.0

mydb = database()


# AWS IoT certificate based connection
myMQTTClient = AWSIoTMQTTClient("123afhlss456")
myMQTTClient.configureEndpoint("a2ytl2z266nk44-ats.iot.us-east-1.amazonaws.com", 8883)
myMQTTClient.configureCredentials("/home/pi/Embedded_Interfaces_Design/Project-3/certs/AmazonRootCA1.pem", "/home/pi/Embedded_Interfaces_Design/Project-3/certs/private.pem.key", "/home/pi/Embedded_Interfaces_Design/Project-3/certs/certificate.pem.crt")
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

#connect and publish
myMQTTClient.connect()
#myMQTTClient.publish("Project3sub", "connected", 0)

class TornadoServer(tornado.web.Application):
    def __init__(self):
        handlers = [(r"/ws", WSHandler), (r"/(humidityplot.png)",tornado.web.StaticFileHandler,{'path':'./'}), (r"/(tempplot.png)",tornado.web.StaticFileHandler,{'path':'./'}),]
        settings = {'debug': True}
        super().__init__(handlers, **settings)

    def run(self, port=8888):
        
        self.listen(8888)
        myIP = socket.gethostbyname(socket.gethostname())
        print ('*** Websocket Server Started at %s***' % myIP)
        tornado.ioloop.IOLoop.current().start()
            
#UI = Ui_MainWindow()

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print ('New connection established')
      
    def on_message(self, message):    
        
        data = message

        if (message == "Get Current Sensor Values"):
            ui.sensor()
            if(globals.gtempc == 0 and globals.ghum == 0):
                self.write_message(message + "," + "Sensor Disconnected")
            else:
                datetimeobj=datetime.now()
                allvalues = str(datetimeobj.hour)+":"+str(datetimeobj.minute)+":"+str(datetimeobj.second) + "," + str(globals.gtempc) + " C" + "," + str(globals.ghum)
                self.write_message(message +","+str(allvalues))
        
        elif (message == "Get Last Ten Values"):
            if(count < 10):
                data = data + "," + "Wait for 10 Readings"
                self.write_message(data)
            else:
                mydb.get_last_ten_humi_values(count)
                for humi in globals.humi_list:
                    data = data + "," + str(humi)
                self.write_message(data)
                globals.humi_list.clear()
            
        elif (message == "Get Temp Graph"):
            if(count < 10):
                data = "Wait for 10 Readings"
                self.write_message(data)
            else:
                ui.plottempgraph()
                self.write_message("Graph Available")
            
        elif (message == "Get Humi Graph"):
            if(count < 10):
                data = "Wait for 10 Readings"
                self.write_message(data)
            else:
                ui.plothumgraph()
 
    def on_close(self):
        print ('Connection closed')
 
    def check_origin(self, origin):
        return True
 


#main class
class Ui_MainWindow(object):

    #Function to get values from DHT22
    def sensor(self):
        global disconnectflag
        global humidity,temperature,tempc,tempf
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 4

        for i in range(1,5):
            humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
            if humidity is not None and temperature is not None:
                break

        if humidity is not None and temperature is not None:
            disconnectflag=0
            tempc=round(temperature,2)
            tempf=(tempc * 9)/5 + 32
            if tempunit == "F":
                temperature = (temperature * 9)/5 + 32
                
            globals.gtempc = tempc
            globals.gtempf = tempf
            globals.ghum = round(humidity,2)
            
        else:
            globals.gtempc = 0.0
            globals.gtempf = 0.0 
            globals.ghum = 0
            temperature=0.00
            humidity=0.0
            tempc=0.0
            tempf=0.0
            disconnectflag=1

    #Function to print the real time values when Get Values button is pressed
    def Getvals(self):
        global humidity,temperature,tempc,tempf
        self.sensor()
        datetimeobj=datetime.now()
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.time.setText("    "+str(datetimeobj.hour)+":"+str(datetimeobj.minute)+":"+str(datetimeobj.second))
        self.time.text()
        self.tempval.setText("    "+str(round(temperature,2))+" "+tempunit)
        self.tempval.text()
        self.humval.setText("    "+str(round(humidity,1))+" "+"%")
        self.humval.text()
        
        payload = '{"Topic" : "Data", "Timestamp": "'+ now_str +'","temperature": '+str(round(temperature,2))+' ,"humidity": '+str(round(humidity,1)) +' }'
        print(payload)
        myMQTTClient.publish("Project3sub", payload, 0)
        



    #Change the unit from Celcius to Fahrenheit or vice-versa
    def changetempunit(self):

        global tempunit,temperature,humidity,tempc,tempf,count
        
        datetimeobj1=datetime.now()
        if tempunit == "C":
            tempunit=tempunit.replace("C","F")
            self.ctof.setText("F To C")
            self.HTtempscroll.setValue( (self.HTtempscroll.value()*9)/5 +32)
            self.LTtempscroll.setValue( (self.LTtempscroll.value()*9)/5 +32)
            self.tempval.setText("    "+str(round(tempf,2))+" "+tempunit)
            self.tempval.text()
            self.statusedit.setPlainText("    Reading: "+str(count)+"\n\n"+"    Time: "+str(datetimeobj1.hour)+":"+str(datetimeobj1.minute)+":"+str(datetimeobj1.second)+"\n\n"+"    Temperature: "+str(round(tempf,2))+" "+tempunit + "\n\n" +"    Humidity: "+str(round(humidity,1))+" "+"%")
            
        else:
            self.ctof.setText("C To F")
            tempunit=tempunit.replace("F","C")
            self.HTtempscroll.setValue(((self.HTtempscroll.value()-32)*5)/9)
            self.LTtempscroll.setValue(((self.LTtempscroll.value()-32)*5)/9)
            self.tempval.setText("    "+str(round(tempc,2))+" "+tempunit)
            self.tempval.text()
            self.statusedit.setPlainText("    Reading: "+str(count)+"\n\n"+"    Time: "+str(datetimeobj1.hour)+":"+str(datetimeobj1.minute)+":"+str(datetimeobj1.second)+"\n\n"+"    Temperature: "+str(round(tempc,2))+" "+tempunit + "\n\n" +"    Humidity: "+str(round(humidity,1))+" "+"%")


    #Plot the graph for last ten values of humidity
    def plothumgraph(self):
        if count < 10:
            self.Alarm.setEnabled(1)
            self.Alarm.setText("\n Wait for 10 Readings")
            self.Alarm.text()
            return

        self.humiditygraph.canvas.ax.cla()
        mydb.get_last_ten_humi_values(count)
        y=globals.humi_list
        x=range(0,10)
        self.humiditygraph.canvas.ax.set_title('Humidity Plot')
        self.humiditygraph.canvas.ax.set_xlabel('Readings Index')
        self.humiditygraph.canvas.ax.set_ylabel('Humidity')
        self.humiditygraph.canvas.ax.plot(x,y)
        self.humiditygraph.canvas.draw()
        self.humiditygraph.canvas.print_figure('humidityplot')
        globals.humi_list.clear()
        globals.time_stamp.clear()

    #Plot the graph for last ten values of temperature
    def plottempgraph(self):
        if count < 10:
            self.Alarm.setEnabled(1)
            self.Alarm.setText("\n Wait for 10 Readings")
            self.Alarm.text()
            return

        self.temperaturegraph.canvas.ax.cla()
        mydb.get_last_ten_temp_values(count)
        if tempunit == "C":
            y=globals.tempc_list
            x=range(0,10)
            self.temperaturegraph.canvas.ax.set_ylabel('Temperature (C)')
        if tempunit == "F":
            y=globals.tempf_list
            x=range(0,10)
            self.temperaturegraph.canvas.ax.set_ylabel('Temperature (F)')

        self.temperaturegraph.canvas.ax.set_title('Temperature Plot')
        self.temperaturegraph.canvas.ax.set_xlabel('Readings Index')

        self.temperaturegraph.canvas.ax.plot(x,y)
        self.temperaturegraph.canvas.draw()
        self.temperaturegraph.canvas.print_figure('tempplot')
        globals.tempc_list.clear()
        globals.tempf_list.clear()
        globals.time_stamp.clear()

    #Print timestamp, temp and humidity on the status line and report if sensor is disconnected
    def printvals(self):
        global humidity,temperature,tempc,tempf
        self.Alarm.setText("\n     ")
        self.Alarm.text()
        self.Alarm.setDisabled(1)
        self.sensor()
        datetimeobj1=datetime.now()
        now = datetime.utcnow()
        now_str = now.strftime('%Y-%m-%dT%H:%M:%SZ')
        formatted_time = datetimeobj1.strftime('%H:%M:%S')
        if disconnectflag == 0:
            self.statusedit.setPlainText("    Reading: "+str(count)+"\n\n"+"    Time: "+str(datetimeobj1.hour)+":"+str(datetimeobj1.minute)+":"+str(datetimeobj1.second)+"\n\n"+"    Temperature: "+str(round(temperature,2))+" "+tempunit + "\n\n" +"    Humidity: "+str(round(humidity,1))+" "+"%")

            #setting data for Lambda
            payload = '{"Topic" : "Data","Timestamp": "' + now_str + '" ,"temperature": ' + str(round(temperature,2)) + ',"humidity": '+ str(round(humidity,1)) +'}'
            print(payload)
            myMQTTClient.publish("Project3sub", payload, 0)


            mydb.add_values_db(tempc, tempf, humidity, formatted_time)

            if temperature>self.HTtempscroll.value() or temperature<self.LTtempscroll.value() or humidity>self.HThumscroll.value() or humidity<self.LThumscroll.value():
                self.Alarm.setEnabled(1)
                self.Alarm.setText("\n            !!ALARM!! ")
                self.Alarm.text()
                if temperature>self.HTtempscroll.value():
                    payload = '{"Topic" : "Alert","Timestamp": "' + now_str + '","temperature alert": ' + str(self.HTtempscroll.value())  +',"temperature trigger": ' + str(round(temperature,2)) + ' }'
                    print(payload)
                    myMQTTClient.publish("Project3sub", payload, 0)
                    
                if humidity>self.HThumscroll.value():
                    payload = '{"Topic" : "Alert","Timestamp": "' + now_str + '","humidity alert": '+ str(self.HThumscroll.value()) + ',"humidity trigger": '+ str(round(humidity,1)) + ' }'
                    print(payload)
                    myMQTTClient.publish("Project3sub", payload, 0)
                
            if self.HThumscroll.value()<=self.LThumscroll.value():
                self.Alarm.setEnabled(1)
                self.Alarm.setText("\n Check Humidity Threshold")
                self.Alarm.text()

            if  self.HTtempscroll.value()<=self.LTtempscroll.value():
                self.Alarm.setEnabled(1)
                self.Alarm.setText("\n Check Temperature Threshold")
                self.Alarm.text()
        else:
            mydb.add_values_db(tempc, tempf, humidity, formatted_time)
            self.statusedit.setPlainText("\n\n    SENSOR DISCONNECTED!! ")

    #Counts to 30 for timer to stop
    def counter(self):
        global count
        if count == 30:
            count=0
            self.timer.stop()
            self.refb.setEnabled(True)
            #exit
        else:
            count = count + 1        
            self.printvals()
        globals.gc = count; 

    #refresh the timer to re-start the timer
    def refreshtimer(self):
        mydb.printall(30)
        mydb.delete_values_db()
        os.execl(sys.executable, sys.executable, * sys.argv)

    #setup the GUI
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SensorGUI")
        MainWindow.resize(1287, 819)
        MainWindow.setMinimumSize(QtCore.QSize(1287, 819))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        QtWidgets.qApp.processEvents()
        self.getvalb = QtWidgets.QPushButton(self.centralwidget)
        self.getvalb.setGeometry(QtCore.QRect(230, 180, 99, 30))
        self.getvalb.setObjectName("getvalb")
        self.getvalb.clicked.connect(self.Getvals)
        self.Humlabel = QtWidgets.QLabel(self.centralwidget)
        self.Humlabel.setGeometry(QtCore.QRect(190, 90, 71, 22))
        self.Humlabel.setTextFormat(QtCore.Qt.AutoText)
        self.Humlabel.setObjectName("Humlabel")
        self.templabel = QtWidgets.QLabel(self.centralwidget)
        self.templabel.setGeometry(QtCore.QRect(190, 130, 101, 22))
        self.templabel.setObjectName("templabel")
        self.HTtempscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.HTtempscroll.setGeometry(QtCore.QRect(180, 690, 71, 32))
        self.HTtempscroll.setObjectName("HTtempscroll")
        self.HTtempscroll.setMaximum(99.00)
        self.HTtempscroll.setMinimum(0.00)
        self.HTtempscroll.setValue(32.00)
        self.LTtempscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.LTtempscroll.setGeometry(QtCore.QRect(180, 750, 71, 32))
        self.LTtempscroll.setObjectName("LTtempscroll")
        self.LTtempscroll.setMaximum(99.00)
        self.LTtempscroll.setMinimum(0.00)
        self.LTtempscroll.setValue(22.00)
        self.HTtemp = QtWidgets.QLabel(self.centralwidget)
        self.HTtemp.setGeometry(QtCore.QRect(60, 690, 111, 22))
        self.HTtemp.setObjectName("HTtemp")
        self.LTtemp = QtWidgets.QLabel(self.centralwidget)
        self.LTtemp.setGeometry(QtCore.QRect(60, 750, 111, 22))
        self.LTtemp.setObjectName("LTtemp")
        self.LThum = QtWidgets.QLabel(self.centralwidget)
        self.LThum.setGeometry(QtCore.QRect(980, 750, 111, 22))
        self.LThum.setObjectName("LThum")
        self.HThumscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.HThumscroll.setGeometry(QtCore.QRect(1100, 690, 71, 32))
        self.HThumscroll.setObjectName("HThumscroll")
        self.HThumscroll.setMaximum(99.00)
        self.HThumscroll.setMinimum(0.00)
        self.HThumscroll.setValue(35.00)
        self.LThumscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.LThumscroll.setGeometry(QtCore.QRect(1100, 750, 71, 32))
        self.LThumscroll.setObjectName("LThumscroll")
        self.LThumscroll.setMaximum(99.00)
        self.LThumscroll.setMinimum(0.00)
        self.LThumscroll.setValue(10.00)
        self.HThum = QtWidgets.QLabel(self.centralwidget)
        self.HThum.setGeometry(QtCore.QRect(980, 690, 111, 22))
        self.HThum.setObjectName("HThum")
        self.tempbutton = QtWidgets.QPushButton(self.centralwidget)
        self.tempbutton.setGeometry(QtCore.QRect(40, 640, 106, 30))
        self.tempbutton.setObjectName("tempbutton")
        self.tempbutton.clicked.connect(self.plottempgraph)
        self.humbutton = QtWidgets.QPushButton(self.centralwidget)
        self.humbutton.setGeometry(QtCore.QRect(1030, 640, 99, 30))
        self.humbutton.setObjectName("humbutton")
        self.humbutton.clicked.connect(self.plothumgraph)
        self.temperaturegraph = MplWidget('Temperature Plot', 'Reading', 'Temperature', self.centralwidget)
        self.temperaturegraph.setGeometry(QtCore.QRect(5, 230, 631, 400))
        self.temperaturegraph.setObjectName("temperaturegraph")

        self.humiditygraph = MplWidget('Humidity Plot', 'Reading', 'Humidity', self.centralwidget)
        self.humiditygraph.setGeometry(QtCore.QRect(675, 230, 571, 400))
        self.humiditygraph.setObjectName("humiditygraph")

        self.refb = QtWidgets.QPushButton(self.centralwidget)
        self.refb.setGeometry(QtCore.QRect(1080, 120, 99, 30))
        self.refb.setObjectName("refb")
        self.refb.setEnabled(False)
        self.refb.clicked.connect(self.refreshtimer)
        self.humval = QtWidgets.QLineEdit(self.centralwidget)
        self.humval.setGeometry(QtCore.QRect(300, 80, 81, 32))
        self.humval.setObjectName("humval")
        self.tempval = QtWidgets.QLineEdit(self.centralwidget)
        self.tempval.setGeometry(QtCore.QRect(300, 120, 91, 32))
        self.tempval.setObjectName("tempval")
        self.Alarm = QtWidgets.QLineEdit(self.centralwidget)
        self.Alarm.setGeometry(QtCore.QRect(550, 670, 230, 61))
        self.Alarm.setObjectName("Alarm")
        self.Alarm.setEnabled(0)
        self.time = QtWidgets.QLineEdit(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(300, 40, 113, 32))
        self.time.setObjectName("time")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(190, 50, 68, 22))
        self.label.setObjectName("label")
        self.ctof = QtWidgets.QPushButton(self.centralwidget)
        self.ctof.setGeometry(QtCore.QRect(230, 640, 101, 30))
        self.ctof.setObjectName("ctof")
        self.ctof.clicked.connect(self.changetempunit)
        self.statusedit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.statusedit.setGeometry(QtCore.QRect(740, 50, 271, 170))
        self.statusedit.setObjectName("statusedit")
        self.statuslabel = QtWidgets.QLabel(self.centralwidget)
        self.statuslabel.setGeometry(QtCore.QRect(820, 20, 111, 22))
        self.statuslabel.setObjectName("statuslabel")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.timer = QTimer()
        self.timer.timeout.connect(self.counter)
        self.timer.start(15000)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.getvalb.setText(_translate("MainWindow", "Get Values"))
        self.Humlabel.setText(_translate("MainWindow", "Humidity : "))
        self.templabel.setText(_translate("MainWindow", "Temperature :"))
        self.HTtemp.setText(_translate("MainWindow", "High Threshold:"))
        self.LTtemp.setText(_translate("MainWindow", "Low Threshold :"))
        self.LThum.setText(_translate("MainWindow", "Low Threshold :"))
        self.HThum.setText(_translate("MainWindow", "High Threshold:"))
        self.tempbutton.setText(_translate("MainWindow", "Temperature"))
        self.humbutton.setText(_translate("MainWindow", "Humidity"))
        self.refb.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "Time :"))
        self.ctof.setText(_translate("MainWindow", "C To F"))
        self.statuslabel.setText(_translate("MainWindow", "Sensor Status :"))


# application = tornado.web.Application([
#     (r'/ws', WSHandler),
#     (r"/(humidityplot.png)",tornado.web.StaticFileHandler,{'path':'./'}),
#     (r"/(tempplot.png)",tornado.web.StaticFileHandler,{'path':'./'}),
# ])

ui = Ui_MainWindow()

def run_UI():
    import sys
    globals.global_init()
    mydb.delete_values_db()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

server = TornadoServer()

def run_tornado():
    asyncio.set_event_loop(asyncio.new_event_loop())
    server.run()
    # http_server = tornado.httpserver.HTTPServer(application)
    # http_server.listen(8888)
    # myIP = socket.gethostbyname(socket.gethostname())
    # print ('*** Websocket Server Started at %s***' % myIP)
    # tornado.ioloop.IOLoop.current().start()


if __name__ == "__main__":

    thread_1 = threading.Thread(target = run_UI)
    thread_2 = threading.Thread(target = run_tornado)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    print("Program Done")
