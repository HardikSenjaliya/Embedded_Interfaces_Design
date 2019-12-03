#!/usr/bin/python3

#Libraries
import RPi.GPIO as GPIO
import time
import datetime
import picamera

#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
servoPIN = 17
 

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
    
def setup_distance_sensor():    
    #GPIO Mode (BOARD / BCM)
    GPIO.setmode(GPIO.BCM)
 

    #set GPIO direction (IN / OUT)
    GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
    GPIO.setup(GPIO_ECHO, GPIO.IN)
    
def setup_servo():

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(servoPIN, GPIO.OUT)
 
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
 
if __name__ == '__main__':
    
    
    setup_distance_sensor()
    
    try:
        while True:
            dist = get_distance()
            print ("Measured Distance = %.1f cm" % dist)
            if(dist < 80):
                capture_image()
                break
            time.sleep(1)
 
    # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()
