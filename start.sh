#! /bin/bash

#set up can
sudo ip link set can0 up type can bitrate 460800

#clear previous logs
rm -rf *.log

#prepare db and dbMS
#rm test.db
#python setupdb.py
#python databaseMS.py &

#-t A	-	for displaing time w/ date
#-l	-	for logging; need to be run w/ sudo; prints output to a .log file
#-x	-	for extra info; RX-receiving; TX-transmitting
candump can0 -t A | python3 /home/pi/EnvSen/translateFrames.py
#candump can0 -t a -x | python /home/pi/EnvSen/translateFrames.py
