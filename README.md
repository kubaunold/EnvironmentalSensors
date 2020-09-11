# ETD_EnvironmentalSensor
Project in Python consisting of smaller apps talking to each other (micro-services) that enables reading measurements from Hum&Temp sensor and displaying them on a webpage.

### Steps for creating project ###
# Download repo
git clone <adres_url>

# Create venv and install required packages
python3 -m venv venv
source ./venv/bin/activate
pip install --upgrade pip
pip3 install -r ./requirements.txt

# permanent alias
nano ~/.bashrc
alias venv="source ~/EnvironmentalSensors/venv/bin/activate"
#reboot or type `source ~/.bashrc`

# CAN config (for temp&hum sensor) //add or uncomment
dtparam=spi=on
dtoverlay=mcp2515-can0,oscillator=8000000,interrupt=25,spimaxfrequency=1000000

sudo apt update
sudo modprobe mcp251x
sudo apt install can-utils   #worth rebooting now
sudo ip link set can0 up type can bitrate 460800
candump can0 -t A

# some bug fix
sudo apt-get install libatlas-base-dev

# running app
./start.sh