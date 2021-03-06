#!/usr/bin/python3

import boto3
import RPi.GPIO as GPIO
import time
import datetime
import picamera
import tornado.httpserver
import tornado.websocket
import tornado.ioloop  
import tornado.web
import asyncio
import socket
import MySQLdb
import threading


GPIO.setwarnings(False)

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)        
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

led = 12
GPIO.setmode(GPIO.BCM)
# set up GPIO output channel
GPIO.setup(led, GPIO.OUT)


bucket_name = 'eid-image-rekognition' 
collection_id = 'user_profile_images'

threshold = 97
maxFaces=1

s3Client = boto3.client('s3')
rekoClient = boto3.client('rekognition')

statust = ' '
stat=0


class WSHandler(tornado.websocket.WebSocketHandler):
    
    
    def open(self):
        
        global count,stat
        print ('New connection established (Tornado <--> Client)')
                        
        self.write_message("Unrecognized")
        p.ChangeDutyCycle(2.5)
                
        #while loop to keep the camera going and update the cliet about match/no match images 
        while True:
                
            if(stat == 1):
                print("Unlock on Client")
                stat=0
                self.write_message(statust)
                p.ChangeDutyCycle(12.5)
                time.sleep(5)
    
                self.write_message("Unrecognized")
                print("Locked")
                p.ChangeDutyCycle(2.5)        

      
    def on_message(self, message):
        data = message
 
 
    def on_close(self):
        print ('Connection closed (Tornado <--> Client)')
 
    def check_origin(self, origin):
        return True
            

class cameraclass(object):

    def setup_servo(self):
    
        p.start(2.5) # Initialization
        p.ChangeDutyCycle(2.5)
        time.sleep(0.1)
        
    
    
    def capture_image(self):
        GPIO.output(12, GPIO.HIGH)
    #with picamera.PiCamera() as camera:
        camera = picamera.PiCamera()
        camera.resolution = (1280, 720)
        camera.framerate = 30
        # Wait for the automatic gain control to settle
        time.sleep(2)
        # Now fix the values
        camera.shutter_speed = camera.exposure_speed
        camera.exposure_mode = 'off'
        g = camera.awb_gains
        camera.awb_mode = 'off'
        camera.awb_gains = g
        timestamp = datetime.datetime.now().strftime("%m_%d_%Y_%H_%M_%S")
        # Finally, take several photos with the fixed settings
        camera.capture(timestamp + '.jpg')

        
        local_image = (timestamp+'.jpg')
        #local_image = 'Hardik_Portrait.JPG'
        
        print ("Captured") 
        print(local_image)
        
        GPIO.output(12, GPIO.LOW)
              
        cam.find_face_in_collection(bucket_name, local_image, collection_id, camera)
  

     
    def get_distance(self):
        GPIO.setmode(GPIO.BCM)
        #set GPIO direction (IN / OUT)
        GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(GPIO_ECHO, GPIO.IN)
        
    
        # set Trigger to HIGH
        GPIO.output(GPIO_TRIGGER, True)
     
        # set Trigger after 0.01ms to LOW
        time.sleep(0.00001)
        GPIO.output(GPIO_TRIGGER, False)
     
        StartTime = time.time()
        StopTime = time.time()
     
        # save StartTime
        while GPIO.input(GPIO_ECHO) == 0:
            StartTime = time.time()
     
        # save time of arrival
        while GPIO.input(GPIO_ECHO) == 1:
            StopTime = time.time()
     
        # time difference between start and arrival
        TimeElapsed = StopTime - StartTime
        # multiply with the sonic speed (34300 cm/s)
        # and divide by 2, because there and back
        distance = (TimeElapsed * 34300) / 2
     
        return distance
                    
    def find_face_in_collection(self,bucket, image, collection_id, camera):
        
        global statust,stat   
                    
                
        camera.close() #close the camera object
        
        try:     

            with open(image, 'rb') as image:
                response=rekoClient.search_faces_by_image(CollectionId=collection_id,
                                        Image={'Bytes': image.read()},
                                        FaceMatchThreshold=threshold,
                                        MaxFaces=maxFaces)
        
        
            faceMatches=response['FaceMatches']
            print ('Matching faces ...')
            stat=0
            for match in faceMatches:
                    print ('FaceId:' + match['Face']['FaceId'])
                    print('Name:' + match['Face']['ExternalImageId'])
                    print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
                    if(match['Similarity'] > 80):
                        print('Unlock')
                        statust= match['Face']['ExternalImageId']
                        statust = statust[:-4] 
                        stat=1
                        
    
                        image = ''
            
            if(stat==0):
                statust= 'no'

            
            return True
        
        except:
            print("Make sure there is at least one face in the image")
            
            return False

            
    
    def upload_to_aws(self,local_image, bucket, s3_file):
    
        try:
            s3Client.upload_file(local_image, bucket, s3_file)
            print("Upload Successful")
            return True
        except FileNotFoundError:
            print("The file was not found") 
            return False
        except NoCredentialsError:
            print("Credentials not available")
            return False

application = tornado.web.Application([
    (r'/ws', WSHandler),
])
 

cam = cameraclass()

def runtornado():
    
    asyncio.set_event_loop(asyncio.new_event_loop())
    http_server = tornado.httpserver.HTTPServer(application)
    http_server.listen(8889)
    myIP = socket.gethostbyname(socket.gethostname())
    print ('*** Tornado Websocket Server Started at %s***' % myIP)
    tornado.ioloop.IOLoop.current().start()
    
def runcam():
    
    global stat

    cam.setup_servo()
    GPIO.output(12, GPIO.LOW)
    
    try:
        while True:

            dist = cam.get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            if(dist < 100):
                cam.capture_image()
            else:
                p.ChangeDutyCycle(2.5)
                time.sleep(2)

            time.sleep(5)
    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()




if __name__ == '__main__':
    
    thread_1 = threading.Thread(target = runcam)
    thread_2 = threading.Thread(target = runtornado)

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()


    print("Program Done")

