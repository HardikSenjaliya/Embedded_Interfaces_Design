# EID Project 3

## Managing Amazon Web Services with RaspberryPi and sensory values.
### Authors -- Hardik Senjaliya and Isha Sawant

###### This project aims to educate us to use AWS and its services like AWS IoT Core, SNS, SQS and Lambda with the RPi platform and the DHT22 sensor. In this system, the Data and Alert payloads are created by the IoT service, which are then forwarded onto the Lambda service for processing the data payload to SQS (then offloading output on the HTML client) and the alert payload the SNS service (Getting a message and an email) respectively.

##### Installation Instructions and Description:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Project-3
2. For connecting the hardware, place the DHT22 sensor on a breadboard and connect its Pins 1,3 and 4 to RPi3 GPIO 1, 7 and 6 respectively.
   Also connect a 10k resistor between pins 1 and 2 of the sensor.[1]
3. Install python3 and other libraries for mysql, matplotlib to function.
4. The project contains one driver file *Maincode.py* which shall run on the command *./P3init.sh* (bash script to start-up the Project 3 code) and hence initiate the GUI and connect with the MQTT client (also publish the payloads).
   It contains all the primary functions for getting the real-time sensor values, and generating the data and alert payloads for sending over to the lambda service.
5. The GUI send data payload on every 15 seconds and on demanding the real time values, also the alert payload is sent when the temperature or humidity goes higher than the higher threshold   set on the GUI- based on which the HTML shall report a single SQS message or a list of 20 messages when demanded by the user or the number of messages in the SQS Queue at that moment and SNS shall send a message or an email to alert the user based on the alert level.
6. The client also involves a button to convert the temperature units in the displayed tables.
7. On terminating the script with Ctrl+C, the code shall clean up with all values cleared and all processes terminated.


##### Project Work:

While both contributed in the design of the GUI, we also had our own ideas for the following-

*Isha* -- was responsible for setting up the IoT core service with the Lambda service and SNS rules to get the alert and data payloads repectively, and routing the alert payloads to the SNS service as an email and a message on mentioned number.

*Hardik* -- was responsible for looking after the SQS functionality of the system, where the data payloads get displayed on the HTML client and also for the extra credit of displaying the number of messages in the SQS queue.

##### Project Additions:

1. The project includes alert payloads to be displayed not only as a message but also to an email as programmed into the rule for temperature and humidity alerts both.
2. The extra credit has been also added to the system to display the number of messages in the SQS queue on prompted by the user via a button.
3. IoT core and Lambda work together to handle a particular error condition such that if the lambda function is not correctly evoked after the payload has been published then the payload shall be re-published into the IoT error topic as a way to log that error.

##### Project Issues:

1. The most common issue in the system was to set-up the lambda rule with the IoT core service and to get the entire project flow working with the test MQTT client, but eventually the AWS documentation on the Web helped a lot with its proper procedure based explanation.
2. Second issue was with SQS to get the HTTP bridge to work and transport the SQS queue messages onto the client, but this issue was also tacked with the help of online and provided references.

