#!/bin/bash

# Authors -- Isha Sawant and Hardik Senjaliya
# Description -- To start-up Python app and two servers.


#function handler()
#{
#    # echo "here"
#    kill -9 $PID1 $PID2 $PID3
#}
#
#trap handler SIGINT
#sleep 3s &
#wait
#
#python3 Maincode.py &
#PID1=$!
#echo $PID1
#
#python3 tornado_webserver.py &
#PID2=$!
#echo $PID2
#
#node nodeserver.js &
#PID3=$!
#echo $PID3
#
#while kill -0 $PID1 $PID2 $PID3 > /dev/null 2>&1
#do
#    wait $PID1 $PID2 $PID3
#done
#
#echo " ** END ** "

function handler()
{
    # echo "here"
    kill -9 $PID1 $PID3
}

trap handler SIGINT
sleep 3s &
wait

python3 Maincode.py &
PID1=$!
echo $PID1

node nodeserver.js &
PID3=$!
echo $PID3

while kill -0 $PID1 $PID3 > /dev/null 2>&1
do
    wait $PID1 $PID3
done

echo " ** END ** "
