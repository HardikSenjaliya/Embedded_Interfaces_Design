# EID Project 6

## Face Recognition Door Access System
### Authors -- Hardik Senjaliya and Isha Sawant

##### This project aims to work as security system for any organisation or home. It uses a face recognition service to identify authorized personnel and unlock the door only on a good match in the features. Based on a Raspberry Pi, the project uses an ultrasonic sensor to measure the dustance of the person standing in front of the camera, once a close distance is achieved the LED glows to indicate an image capture by the connected camera. This image then is evaluated by the AWS service (if present in the database or not) and based on the results, the servo motor locks or unlocks. The control being in the admin's hand, shall result in addition or removal of users to the database, hence allowing them to either unlock the system themselves or lose their authority. This system is a high end prototype to a system that could give an idea for security systems be free of keycards or IDs.

#### Notes and Installation Instructions:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Face-Recognition-Access-System
2. Install python3, tornado webserver, boto3 client (for AWS), pi-camera, time and gpio supporting libraries.
3. The project contains one driver file *upload_awss3.py* which shall run on the command *./Project_init.sh* (startup shell script) and hence initiate the camera, ultrasonic sensor, servo motor and tornado webserver.
4. It contains a threading mechanism that allows the tornado server and the camera-hardware-motor-lock/unlock code to work simultaneously.
5. The .html file located in the folder is the Client GUI that is dependent on the .css design file, my_jquery.js and tornado webserver messages.
