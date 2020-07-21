#script translates CAN raw gates to human and puts them in db
import sys
import numpy as np
import json
from datetime import date, time, datetime
import requests


# "constatnt" variables used for printing result 
CELS = str("\u00b0C")  #sign for Celsius degrees
PERC = str("%")        #sign for humidity

def obtainMeasurement():
    dataS = sys.stdin.readline()
    print(dataS)
    
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

if __name__ == "__main__":
    myApp = "http://127.0.0.1:5000/receiveMeasurement"
    while(1):
        measurementDict = obtainMeasurement()
        measurementJson = json.dumps(measurementDict)
        print(measurementJson)
        print('')
        print('')
        #it has to be python-dict as a payload!
        r = requests.post(myApp, data=measurementDict)
