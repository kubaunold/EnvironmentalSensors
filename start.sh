#! /bin/bash

# activate virtual environment
source ~/EnvironmentalSensors/venv/bin/activate 

# create log/ directory if not yet created
DIR="./log/"
if [ -d "$DIR" ]; then
  ### Take action if $DIR exists ###
  echo "Log directory ${DIR} exists. Proceedeing..."
  echo ""
else
  ###  Control will jump here if $DIR does NOT exists ###
  echo "Could not find ${DIR} directory. Creating one in order to continue."
  mkdir ./log/
  echo "Driectory ${DIR} created successfully."
#   exit 1
fi

# set up can
sudo ip link set can0 up type can bitrate 460800

# capture SIGINT
handler()
{
    pkill -f webApp.py
    pkill -f translateFrames.py
    sleep 1
    pkill -f databaseMS.py
}
trap handler SIGINT

# clear previous logs
#rm -rf log/*.log

#-t A	-	for displaing time w/ date
#-l	    -	for logging; need to be run w/ sudo; prints output to a .log file
#-x 	-	for extra info; RX-receiving; TX-transmitting
python databaseMS.py & python webApp.py & candump can0 -t A | python3 translateFrames.py

#screen



