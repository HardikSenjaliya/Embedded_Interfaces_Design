#!/bin/bash

# Authors -- Isha Sawant and Hardik Senjaliya



function handler()
{
    # echo "here"
    kill -9 $PID1
}

trap handler SIGINT
sleep 3s &
wait

python3 upload_awss3.py &
PID1=$!
echo $PID1


while kill -0 $PID1 > /dev/null 2>&1
do
    wait $PID1
done

echo " ** END ** "
