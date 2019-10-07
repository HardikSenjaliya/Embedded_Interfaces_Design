## EID Project 2


## Implementing communication between a HTML Client with Tornado and Node.JS servers.
### Authors -- Hardik Senjaliya and Isha Sawant

###### This project focuses on bidirectional communication between Tornado and Node.JS websockets with HTML client and also MySQL database operations with the Python App which includes DHT22 sensor interfaced with the Raspberry Pi board.

##### Installation Instructions and Description:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Project-2
2. For connecting the hardware, place the DHT22 sensor on a breadboard and connect its Pins 1,3 and 4 to RPi3 GPIO 1, 7 and 6 respectively.
   Also connect a 10k resistor between pins 1 and 2 of the sensor.
3. Install python3 and other libraries for mysql to function, npm install for nodejs code and pip install tornado for the tornado server to work.
4. The project contains one driver file *P2init.sh* which is a shell script to start-up : Maincode.py (python app), nodeserver.js (node.js server) and tornado_webserver.js (tornado server).
5. After the init shell script, get to the web browser to open the HTML client (which is designed using a .css styling sheet, .html file and a jquery JavaScript file to handle all labels/inputs/buttons on the window), which shall then ensure the servers getting connecting to the client, after which the user can use the buttons to get values as needed.
6. The Tornado server shall give the real-time sensor values and Node.JS gives the last recorded value from the sql database; after 10 values of recording from the App, the datasets can be compared to check the duration time of the nodejs and tornado routes for getting humidity values, also, locally the temperature unit can be altered and all values can be cleared if needed.   
7. On terminating the script with Ctrl+C, the code shall clean up with all values cleared and all processes terminated.

##### Project Work:

While both contributed in the design of the GUI of the HTML client (.css/.html files) and the compare-dataset functionality for the respective servers, we also had our own ideas for the following-

*Isha* -- was responsible for all the Node.JS operations in the system, including the configuration for connecting the server and client, functionality for retrieving values from the database and creating a start-up bash script for the system that takes care of the SIGINT termination signal.

*Hardik* -- was responsible for configuring the tornado server with the client, and all its operations that consist of getting real-time sensor values, getting the plots from the Python App for temperature/humidity and clearing data at the end of the script.

##### Project Additions and Errors Handled:

1. The user shall get notified about the sensor being disconnected with zeroed values for those respective temperature/humidity readings.
2. The unit of temperature shall be altered only locally on HTML client as and when needed and shall be updated in Celcius again if prompted so by the user.
3. Lastly, we also have added the extra credit functionality that allows the user to get the plots for temperature or humidity using two buttons on the client window.

