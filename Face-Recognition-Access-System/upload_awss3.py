#!/usr/bin/python3

import boto3
import RPi.GPIO as GPIO
import time
import datetime
import picamera


#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
servoPIN = 17
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)        
p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz

#local_image = '12_03_2019_16_04_42.jpg'
bucket_name = 'eid-image-rekognition' 
collection_id = 'user_profile_images'

threshold = 97
maxFaces=1

s3Client = boto3.client('s3')
rekoClient = boto3.client('rekognition')

def setup_servo():

    p.start(2.5) # Initialization
    p.ChangeDutyCycle(2.5)
    time.sleep(0.1)
    


def capture_image():
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
    
    return (timestamp+'.jpg')
    
def setup_distance_sensor():    
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
 

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    

 
def get_distance():
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

def find_face_in_collection(bucket, image, collection_id):
#
#    response=rekoClient.search_faces_by_image(CollectionId=collection_id,
#                                Image={'S3Object':{'Bucket':bucket,'Name':image}},
#                                FaceMatchThreshold=threshold,
#                                MaxFaces=maxFaces)
#
    with open(image, 'rb') as image:
        response=rekoClient.search_faces_by_image(CollectionId=collection_id,
                                Image={'Bytes': image.read()},
                                FaceMatchThreshold=threshold,
                                MaxFaces=maxFaces)


    faceMatches=response['FaceMatches']
    print ('Matching faces')
    for match in faceMatches:
            print ('FaceId:' + match['Face']['FaceId'])
            print('Name:' + match['Face']['ExternalImageId'])
            print ('Similarity: ' + "{:.2f}".format(match['Similarity']) + "%")
            if(match['Similarity'] > 97):
                print('Unlock')
                p.ChangeDutyCycle(12.5)
                time.sleep(5)
                p.stop()
                GPIO.cleanup()


def upload_to_aws(local_image, bucket, s3_file):

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
        
        

if __name__ == '__main__':

    setup_distance_sensor()
    setup_servo()
    
    try:
        while True:
            dist = get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            if(dist < 80):
                local_image = capture_image()
                
                print ("Captured")
                break
            time.sleep(1)
    
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
        
    find_face_in_collection(bucket_name, local_image, collection_id)
    



