#!/usr/bin/python3

import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import socket
import MySQLdb
from datetime import datetime

        

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print ('New connection established (Tornado <--> Client)')
      
    def on_message(self, message):
        
        
        data = message
        
       # eidDB = MySQLdb.connect(host="localhost",
        #             user="hardyk",
         #            passwd="mysql123",
          #           database="EID_projectDB"
      #  )

       # mycur = eidDB.cursor()

        
 
    def on_close(self):
        print ('Connection closed (Tornado <--> Client)')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 

 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8888)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Tornado Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
