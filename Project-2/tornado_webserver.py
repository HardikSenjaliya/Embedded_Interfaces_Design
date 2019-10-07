#!/usr/bin/python3

import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import socket
import MySQLdb
from Maincode import Ui_MainWindow
import Adafruit_DHT
from datetime import datetime
import globals

vals = Ui_MainWindow()
globals.gunit=0;
        

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print ('New connection established (Tornado <--> Client)')
      
    def on_message(self, message):
        
        
        data = message
        
        eidDB = MySQLdb.connect(host="localhost",
                     user="hardyk",
                     passwd="mysql123",
                     database="EID_projectDB"
        )

        mycur = eidDB.cursor()
        if (message == "Get Current Sensor Values"):
            vals.sensor()
       
            datetimeobj=datetime.now()
            allvalues = str(datetimeobj.hour)+":"+str(datetimeobj.minute)+":"+str(datetimeobj.second) + "," + str(globals.gtempc) + " C" + "," + str(globals.ghum)
            self.write_message(message +","+str(allvalues))
        
        elif (message == "Get Last Ten Values"):
            print ("Getting Last 10 values from Tornado")
            
            mycur.execute("SELECT * FROM sensor_values ORDER BY formatted_time DESC LIMIT 10")
            for row in mycur.fetchall():
                data = data + "," + str(row[4])
          
            self.write_message(data)
            
            
            
 
    def on_close(self):
        print ('Connection closed (Tornado <--> Client)')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
    (r"/(humidityplot.png)",tornado.web.StaticFileHandler,{'path':'./'}),
    (r"/(tempplot.png)",tornado.web.StaticFileHandler,{'path':'./'}),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Tornado Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
