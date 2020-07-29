#! /bin/bash

#set up can
sudo ip link set can0 up type can bitrate 460800

#capture SIGINT
handler()
{
    pkill -f webApp.py
    pkill -f translateFrames.py
    sleep 1
    pkill -f databaseMS.py
}
trap handler SIGINT

#clear previous logs
#rm -rf log/*.log

#-t A	-	for displaing time w/ date
#-l	    -	for logging; need to be run w/ sudo; prints output to a .log file
#-x 	-	for extra info; RX-receiving; TX-transmitting
python databaseMS.py & python webApp.py & candump can0 -t A | python3 /home/pi/EnvSen/translateFrames.py





