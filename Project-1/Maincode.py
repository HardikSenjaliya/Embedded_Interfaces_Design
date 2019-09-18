#!/usr/bin/python3

# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Project1.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime
from PyQt5.QtCore import pyqtSlot
import Adafruit_DHT
from datetime import datetime
import threading

tempunit = "C"
count = 0
humidity = 0.0
temperature = 0.0
disconnectflag=0

class Ui_MainWindow(object):

    def sensor(self):
        global disconnectflag
        global humidity,temperature
        DHT_SENSOR = Adafruit_DHT.DHT22
        DHT_PIN = 4
        humidity, temperature = Adafruit_DHT.read_retry(DHT_SENSOR, DHT_PIN)

        if humidity is not None and temperature is not None:
            disconnectflag=0
            if tempunit == "F":
                temperature = (temperature * 9)/5 + 32
        else:
            disconnectflag=1

    def Getvals(self):
        global humidity,temperature
        self.sensor()
        datetimeobj=datetime.now()
        self.time.setText("    "+str(datetimeobj.hour)+":"+str(datetimeobj.minute)+":"+str(datetimeobj.second))
        self.time.text()
        self.tempval.setText("    "+str(round(temperature,2))+" "+tempunit)
        self.tempval.text()
        self.humval.setText("    "+str(round(humidity,1))+" "+"%")
        self.humval.text()


    def changetempunit(self):
        global tempunit
        if tempunit == "C":
            tempunit=tempunit.replace("C","F")
        else:
            tempunit=tempunit.replace("F","C")

    def humiditygraph(self):
        print("Humidity MySQL graph")

    def tempgraph(self):
        print("Temperature MySQL graph")

    def printvals(self):
        global humidity,temperature
        self.sensor()
        if disconnectflag == 0:
            datetimeobj1=datetime.now()
            self.statusedit.setPlainText("    Reading: "+str(count)+"\n\n"+"    Time: "+str(datetimeobj1.hour)+":"+str(datetimeobj1.minute)+":"+str(datetimeobj1.second)+"\n\n"+"    Temperature: "+str(round(temperature,2))+" "+tempunit + "\n\n" +"    Humidity: "+str(round(humidity,1))+" "+"%")
        else:
            self.statusedit.setPlainText("    SENSOR DISCONNECTED!! ")


    def counter(self):
        global count
        if count == 2:
            count=0
            self.timer.stop()
            self.refb.setEnabled(True)
        else:
            count = count + 1
            self.printvals()

    def refreshtimer(self):
        self.timer.start(15000)
        self.counter()


    def setupUi(self, MainWindow):
        MainWindow.setObjectName("SensorGUI")
        MainWindow.resize(1287, 819)
        MainWindow.setMinimumSize(QtCore.QSize(1287, 819))
        MainWindow.setStyleSheet("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        QtWidgets.qApp.processEvents()
        self.getvalb = QtWidgets.QPushButton(self.centralwidget)
        self.getvalb.setGeometry(QtCore.QRect(130, 180, 99, 30))
        self.getvalb.setObjectName("getvalb")
        self.getvalb.clicked.connect(self.Getvals)
        self.Humlabel = QtWidgets.QLabel(self.centralwidget)
        self.Humlabel.setGeometry(QtCore.QRect(90, 100, 71, 22))
        self.Humlabel.setTextFormat(QtCore.Qt.AutoText)
        self.Humlabel.setObjectName("Humlabel")
        self.templabel = QtWidgets.QLabel(self.centralwidget)
        self.templabel.setGeometry(QtCore.QRect(90, 140, 101, 22))
        self.templabel.setObjectName("templabel")
        self.HTtempscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.HTtempscroll.setGeometry(QtCore.QRect(180, 500, 71, 32))
        self.HTtempscroll.setStyleSheet("font: 75 italic 12pt \"PibotoLt\";\n"
"font: 12pt \"PibotoLt\";")
        self.HTtempscroll.setObjectName("HTtempscroll")
        self.LTtempscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.LTtempscroll.setGeometry(QtCore.QRect(180, 560, 71, 32))
        self.LTtempscroll.setObjectName("LTtempscroll")
        self.HTtemp = QtWidgets.QLabel(self.centralwidget)
        self.HTtemp.setGeometry(QtCore.QRect(60, 500, 111, 22))
        self.HTtemp.setObjectName("HTtemp")
        self.LTtemp = QtWidgets.QLabel(self.centralwidget)
        self.LTtemp.setGeometry(QtCore.QRect(60, 560, 111, 22))
        self.LTtemp.setObjectName("LTtemp")
        self.LTtemp_2 = QtWidgets.QLabel(self.centralwidget)
        self.LTtemp_2.setGeometry(QtCore.QRect(980, 550, 111, 22))
        self.LTtemp_2.setObjectName("LTtemp_2")
        self.HThumscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.HThumscroll.setGeometry(QtCore.QRect(1100, 490, 71, 32))
        self.HThumscroll.setObjectName("HThumscroll")
        self.LThumscroll = QtWidgets.QDoubleSpinBox(self.centralwidget)
        self.LThumscroll.setGeometry(QtCore.QRect(1100, 550, 71, 32))
        self.LThumscroll.setObjectName("LThumscroll")
        self.HThum = QtWidgets.QLabel(self.centralwidget)
        self.HThum.setGeometry(QtCore.QRect(980, 490, 111, 22))
        self.HThum.setObjectName("HThum")
        self.tempbutton = QtWidgets.QPushButton(self.centralwidget)
        self.tempbutton.setGeometry(QtCore.QRect(130, 350, 106, 30))
        self.tempbutton.setObjectName("tempbutton")
        self.tempbutton.clicked.connect(self.tempgraph)
        self.humbutton = QtWidgets.QPushButton(self.centralwidget)
        self.humbutton.setGeometry(QtCore.QRect(1040, 360, 99, 30))
        self.humbutton.setObjectName("humbutton")
        self.humbutton.clicked.connect(self.humiditygraph)
        self.Temperaturegraph = QtWidgets.QGraphicsView(self.centralwidget)
        self.Temperaturegraph.setGeometry(QtCore.QRect(490, 50, 256, 192))
        self.Temperaturegraph.setObjectName("Temperaturegraph")
        self.Humiditygraph = QtWidgets.QGraphicsView(self.centralwidget)
        self.Humiditygraph.setGeometry(QtCore.QRect(490, 310, 256, 192))
        self.Humiditygraph.setObjectName("Humiditygraph")
        self.refb = QtWidgets.QPushButton(self.centralwidget)
        self.refb.setGeometry(QtCore.QRect(1110, 50, 99, 30))
        self.refb.setObjectName("refb")
        self.refb.setEnabled(False)

        self.refb.clicked.connect(self.refreshtimer)
        self.humval = QtWidgets.QLineEdit(self.centralwidget)
        self.humval.setGeometry(QtCore.QRect(170, 90, 81, 32))
        self.humval.setObjectName("humval")
        self.tempval = QtWidgets.QLineEdit(self.centralwidget)
        self.tempval.setGeometry(QtCore.QRect(200, 130, 91, 32))
        self.tempval.setObjectName("tempval")
        self.Alarm = QtWidgets.QLineEdit(self.centralwidget)
        self.Alarm.setGeometry(QtCore.QRect(540, 580, 161, 61))
        self.Alarm.setObjectName("Alarm")
        self.time = QtWidgets.QLineEdit(self.centralwidget)
        self.time.setGeometry(QtCore.QRect(140, 50, 113, 32))
        self.time.setObjectName("lineEdit")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(90, 60, 68, 22))
        self.label.setObjectName("label")
        self.ctof = QtWidgets.QPushButton(self.centralwidget)
        self.ctof.setGeometry(QtCore.QRect(130, 420, 101, 30))
        self.ctof.setObjectName("ctof")
        self.ctof.setCheckable(True)
        self.ctof.clicked.connect(self.changetempunit)
        self.statusedit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.statusedit.setGeometry(QtCore.QRect(880, 130, 271, 170))
        self.statusedit.setObjectName("statusedit")
        self.statuslabel = QtWidgets.QLabel(self.centralwidget)
        self.statuslabel.setGeometry(QtCore.QRect(970, 100, 111, 22))
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
        self.LTtemp_2.setText(_translate("MainWindow", "Low Threshold :"))
        self.HThum.setText(_translate("MainWindow", "High Threshold:"))
        self.tempbutton.setText(_translate("MainWindow", "Temperature"))
        self.humbutton.setText(_translate("MainWindow", "Humidity"))
        self.refb.setText(_translate("MainWindow", "Refresh"))
        self.label.setText(_translate("MainWindow", "Time :"))
        self.ctof.setText(_translate("MainWindow", "Toggle Unit"))
        self.statuslabel.setText(_translate("MainWindow", "Sensor Status :"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())