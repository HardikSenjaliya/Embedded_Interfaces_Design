#!/usr/bin/python3

import RPi.GPIO as GPIO
from time import sleep

# Needs to be BCM. GPIO.BOARD lets you address GPIO ports by periperal
# connector pin number, and the LED GPIO isn't on the connector
GPIO.setmode(GPIO.BCM)

# set up GPIO output channel
GPIO.setup(12, GPIO.OUT)


# On
GPIO.output(12, GPIO.LOW)

# Wait a bit
sleep(10)

# Off
GPIO.output(12, GPIO.HIGH)

# Wait a bit
sleep(10)

GPIO.output(12, GPIO.LOW)
