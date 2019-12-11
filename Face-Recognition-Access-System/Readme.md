# EID Project 6

## Face Recognition Door Access System
### Authors -- Hardik Senjaliya and Isha Sawant

##### This project aims to recogize faces from a database .

##### Notes and Installation Instructions:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Face-Recognition-Access-System
2. Install python3, tornado webserver, boto3 client (for AWS), pi-camera, time and gpio supporting libraries.
3. The project contains one driver file *upload_awss3.py* which shall run on the command *./Project_init.sh* (startup shell script) and hence initiate the camera, ultrasonic sensor, servo motor and tornado webserver.
   It contains a threading mechanism that allows the tornado server and the camera-hardware-motor-lock/unlock code to work simultaneously.
4. The .html file located in the folder is the Client GUI that is dependent on the .css design file, my_jquery.js and tornado webserver messages.
