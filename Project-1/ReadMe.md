# EID Project 1

## Designing a GUI for Humidity and Temperature Sensing using PyQT5
###Authors -- Hardik Senjaliya and Isha Sawant

######This project aims to educate us with MySql and its database operations and also matplotlib, where the DHT22 sensor interfaced gave
humidity and temperature which shall be fed into the database and then fetched upon request to plot a graph. The system also gives real-
time values and the user can opt to refresh the GUI once 30 reading have been taken.

#####Installation Instructions and Description:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Project-1
2. For connecting the hardware, place the DHT22 sensor on a breadboard and connect its Pins 1,3 and 4 to RPi3 GPIO 1, 7 and 6 respectively.
   Also connect a 10k resistor between pins 1 and 2 of the sensor.[1]
3. Install python3 and other libraries for mysql to function.
4. The project contains one driver file *Maincode.py* which shall run on the command ./Maincode.py and hence initiate the GUI.
   It contains all the primary functions for getting the real-time sensor values, printing on the status line, plotting the graph and setting
   thresholds for both temperature and humidity.
   
   
#####Project Work:

While both contributed in the design of the GUI and the extra credit for changing the temperature unit (On the GUI and the databases/graph
respectively), we also had our own ideas for the following-

*Isha* -- was responsible for generating the code to get the sensor values and print them on the status line using a 15second timer
 also reporting for disconnections and real-time values, and alarming the user in case of values beyond thresholds.

*Hardik* -- was responsible for handling the mysql database for pushing every value in mysqldb as it gets printed into the status line
and matplotlib functions for fetching the values and displaying them on request of the graphs.

#####Project Additions:

1. Added an extra condition for the Alarm, where the humidity or temperature threshold entered cannot converge into each other, if so, 
   displays a different error message to notify the user.
2. A Refresh button for the user to restart the GUI once the database values have been displayed on the terminal and the status line.


