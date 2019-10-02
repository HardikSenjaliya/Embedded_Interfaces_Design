#!/usr/bin/python3

import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import socket
import MySQLdb
#from mysql import database
   
#mydb = database()



class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print ('New connection established')
      
    def on_message(self, message):
        
        data = message
        
        eidDB = MySQLdb.connect(host="localhost",
                     user="hardyk",
                     passwd="mysql123",
                     database="EID_projectDB"
        )

        mycur = eidDB.cursor()
        if (message == "Get Current Sensor Values"):
            mycur.execute("SELECT * FROM sensor_values ORDER BY formatted_time DESC LIMIT 1")
            key, f_time, temp_c, temp_f, humi = mycur.fetchone()
            #print(key,f_time, temp_c, temp_f, humi)
            data = f_time + "," + str(temp_c) + "," + str(humi)
            self.write_message(message +","+str(data))
        
        elif (message == "Get Last Ten Values"):
            mycur.execute("SELECT * FROM sensor_values ORDER BY formatted_time DESC LIMIT 10")
            for row in mycur.fetchall():
                data = data + "," + str(row[4])
                
            self.write_message(data)          
            
 
    def on_close(self):
        print ('Connection closed')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 
 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
