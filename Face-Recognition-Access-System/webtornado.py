#!/usr/bin/python3

import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import socket
import MySQLdb
from datetime import datetime
from upload_awss3 import cameraclass

obj = cameraclass()

        

class WSHandler(tornado.websocket.WebSocketHandler):
    
    def open(self):
        print ('New connection established (Tornado <--> Client)')
        
        while True:
            statust = obj.statusfunc()
            if(statust == 'no'):
                print("Lock on Client")
                self.write_message("Lock")
            else:
                print("Unlock on Client")
                self.write_message(statust)
      
    def on_message(self, message):
        
        
        data = message

        
 
    def on_close(self):
        print ('Connection closed (Tornado <--> Client)')
 
    def check_origin(self, origin):
        return True
 
application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 

 
if __name__ == "__main__":
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Tornado Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
