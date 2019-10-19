#!/bin/bash

# Authors -- Isha Sawant and Hardik Senjaliya
# Description -- To start-up Python app and two servers.


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


while kill -0 $PID1 > /dev/null 2>&1
do
    wait $PID1
done

echo " ** END ** "
