#script translates CAN raw gates to human and puts them in db
import sys
import numpy as np
import json
from datetime import date, time, datetime
import requests
import logging
from sys import stdout  #for dynamic printing in console
from time import sleep

#create logger
LOG_FORMAT = "%(levelname)s %(asctime)s - %(message)s"
logging.basicConfig(filename = "log/translateFrames.log", level = logging.DEBUG, format=LOG_FORMAT, filemode = 'w')
logger = logging.getLogger()


databaseMS_URL = "http://0.0.0.0:5001"

# "constatnt" variables used for printing result 
CELS = str("\u00b0C")  #sign for Celsius degrees
PERC = str("%")        #sign for humidity

def obtainMeasurement():
    dataS = sys.stdin.readline()
    # print(dataS)
    
    #split frame to list
    dataL = dataS.split()
    #print(dataL)
    
    #extract data to human format
    canDate = dataL[0][1:]
    canTime = dataL[1][:-1]
    # canId = int(dataL[3], 16) << 3
    canId = hex(int(dataL[3], 16) << 3)[2:] #needed to be 3x left bit-shifted due to structure
    canLen = int(dataL[4][1:-1])
    
    #measurements (last 6 bytes) as bytearray()
    canData= bytearray()
    for i in range(5, 5+canLen):
        canData.append(int(dataL[i], 16))
    #print(canData)
    
    #measurements split to list and represented binarily
    measurement = " ".join(format(x, "08b") for x in canData)
    #print(measurement)
    measurementSplit = measurement.split(" ")
    #print(measurementSplit)

    #calculate Temperature
    tempHB = measurementSplit[2] #hard-coded position of temp(H)igh (B)its
    tempLB = measurementSplit[3]  #hard-coded posiotion of temp(L)ow (B)its
    tempWholeB = tempHB + tempLB
    jsonTemperature = int(tempWholeB,2)/100.0
    #print(str(temperature) + CELS)
    
    #calculate Humidity
    humHB = measurementSplit[4]
    humLB = measurementSplit[5]
    humWholeB = humHB + humLB
    jsonHumidity = int(humWholeB,2)/100.
    #print(str(humidity) + PERC)

    #fileds ready to be sent
    jsonDatetime = canDate + " " + canTime
    jsonClass = int(canId[:2],16)
    jsonAddress = int(canId[2:4],16)
    jsonCommand = int(canId[4:6],16)
    jsonMask = int(canId[6:8],16)


    #pack to dict, then dump as json
    dataDict = {
            "timestamp": jsonDatetime, 
            "temperature": jsonTemperature,
            "humidity": jsonHumidity,
            "frameClass": jsonClass,
            "frameAddress": jsonAddress,
            "frameCommand": jsonCommand,
            "frameMask": jsonMask
            }
    return dataDict

# def countDown(n):
#     for i in range(n,0,-1):
#         stdout.write("\r%d... " % i)
#         stdout.flush()
#         sleep(1)
#     stdout.write("\n") # move the cursor to the next line


if __name__ == "__main__":
    print("translateFrames: Waiting until the database is up...")
    sleep(5)

    while(1):
        measurementDict = obtainMeasurement()
        # print(json.dumps(measurementDict))
        print("put into db")
        # measurementJson = json.dumps(measurementDict)
        try:
            # send packet
            # it has to be python-dict as a payload!
            r = requests.post(url=databaseMS_URL + "/insertMeasurement", data=measurementDict)
        except ConnectionRefusedError as err:
            error = "ConnectionRefusedError; Reestablishing in 3 seconds..."
            logger.error(error)
            print(error)
            sleep(3)
            # countDown(3)
        except:
            error = "Other error occured; Reestablishing..."
            logger.error(error)
            print("Unable to post request to databaseMS.py.")
            print("Trying to reestablish connection. Wait till timeout is completed...")
            for i in range(101):
                sleep(.03)
                sys.stdout.write("\r%d%%" % i)
                sys.stdout.flush()
            stdout.write("\n") # move the cursor to the next line
        else:
            info = "Frame successfully sent to dataBaseMS"
            logger.info(info)

