# EID Project 1

## Designing a GUI for Humidity and Temperature Sensing using PyQT5
### Authors -- Hardik Senjaliya and Isha Sawant

###### This project aims to educate us with MySql and its database operations and also matplotlib, where the DHT22 sensor interfaced gave humidity and temperature which shall be fed into the database and then fetched upon request to plot a graph. The system also gives real-time values and the user can opt to refresh the GUI once 30 reading have been taken.

##### Installation Instructions and Description:

1. Clone the git repository from the main github like provided and go to path - Embedded_Interfaces_Design->Project-1
2. For connecting the hardware, place the DHT22 sensor on a breadboard and connect its Pins 1,3 and 4 to RPi3 GPIO 1, 7 and 6 respectively.
   Also connect a 10k resistor between pins 1 and 2 of the sensor.[1]
3. Install python3 and other libraries for mysql to function.
4. The project contains one driver file *Maincode.py* which shall run on the command ./Maincode.py and hence initiate the GUI.
   It contains all the primary functions for getting the real-time sensor values, printing on the status line, plotting the graph and setting thresholds for both temperature and humidity. Another file is *mysql.py* which deals with the database and pushes values into the matplotlib widget for the temperature and humidity graphs.
5. The GUI reports if the sensor is disconnected in between of execution (after 15seconds when the sensor function is evoked), the corresponding readings get zeroed values written into the lists and then if the sensor is connected again, they shall resume from the next reading.
   
   
##### Project Work:

While both contributed in the design of the GUI and the extra credit for changing the temperature unit (On the GUI and the databases/graph
respectively), we also had our own ideas for the following-

*Isha* -- was responsible for generating the code to get the sensor values and print them on the status line using a 15second timer
 also reporting for disconnections and real-time values, and alarming the user in case of values beyond thresholds.

*Hardik* -- was responsible for handling the mysql database for pushing every value in mysqldb as it gets printed into the status line
and matplotlib functions for fetching the values and displaying them on request of the graphs.

##### Project Additions:

1. Added an extra condition for the Alarm, where the humidity or temperature threshold entered cannot converge into each other, if so, 
   displays a different error message to notify the user.
2. Extra credit of changing the temperature unit has also been added as a functionality, a button changes its title from *C-To-F* to *F-To-C* whenever pressed and the GUI on the frontend entirely switches the unit with upcoming values.
3. The plots' titles, x-axis and y-axis have been labelled and shall be controlled by a button for getting last 10 values, and respond to the C-To-F or F-To-C buttons as well. 
4. A *Refresh button* for the user to restart the GUI once all the 30 readings have been completed and database values have been displayed on the terminal and the status line.


